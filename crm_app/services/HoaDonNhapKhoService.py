from flask import make_response
from datetime import datetime
from crm_app.services.utils import validate_datetime, isExistId, create_sku
from crm_app.docs.containts import ERROR_CODES, get_error_response  
from crm_app.services.dbService import excute_select_data
from crm_app.models.NhaPhanPhoi import NhaPhanPhoi
from crm_app.models.Kho import Kho
from crm_app.models.HoaDonNhapKho import HoaDonNhapKho
from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app import db

def get_hoa_don_nhap_kho(filter, limit, page, sort, order):
    get_table = 'hoa_don_nhap_kho'
    get_attr = """
        nha_phan_phoi.ten as nha_phan_phoi, nha_phan_phoi.id as nha_phan_phoi_id,
        kho.ten as kho, kho.id as kho_id, ngay_nhap, tong_tien
    """
    query_join = """
        LEFT JOIN nha_phan_phoi ON hoa_don_nhap_kho.nha_phan_phoi_id = nha_phan_phoi.id
        LEFT JOIN kho ON hoa_don_nhap_kho.kho_id = kho.id
    """
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)

    return get_error_response(ERROR_CODES.SUCCESS, result=response_data) 

def post_hoa_don_nhap_kho(nha_phan_phoi_id, kho_id, ngay_nhap, ds_san_pham_nhap):
    print(ds_san_pham_nhap)
    # if validate_datetime(datetime_check=ngay_nhap) is False:
    #     return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 401)
    
    if isExistId(nha_phan_phoi_id, NhaPhanPhoi) is False:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)

    if isExistId(kho_id, Kho) is False:
        return make_response(get_error_response(ERROR_CODES.KHO_NOT_FOUND), 401)
    new_hoa_don = HoaDonNhapKho(nha_phan_phoi_id=nha_phan_phoi_id, kho_id=kho_id, ngay_nhap=ngay_nhap)

    db.session.add(new_hoa_don)
    db.session.flush()

    hoa_don_id = new_hoa_don.id
    counter = 0
    
    for item in ds_san_pham_nhap:
        gia_nhap = item.get("gia_nhap")
        gia_ban = item.get("gia_ban")
        chiet_khau = item.get("chiet_khau")
        total_money = 0
        upc = item.get("upc")    
        if item.get("la_qua_tang") is True:
            gia_nhap = 0
            gia_ban = 0
            chiet_khau = 0

        thanh_tien = add_ct_hoa_don_nhap(upc=upc, ngay_nhap=ngay_nhap, counter=counter, hoa_don_id=hoa_don_id, san_pham_id=item.get("san_pham_id"), ctsp_id=item.get("ctsp_id"), so_luong=item.get("so_luong"), don_vi_tinh=item.get("don_vi_tinh"), ke=item.get("ke"), gia_nhap=gia_nhap, gia_ban=gia_ban, chiet_khau=chiet_khau, la_qua_tang=item.get("la_qua_tang"))
        
        total_money = total_money + thanh_tien
        counter += 1

    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def add_ct_hoa_don_nhap(upc, ngay_nhap, counter, hoa_don_id, san_pham_id, ctsp_id, so_luong, don_vi_tinh, ke, gia_nhap, gia_ban, chiet_khau, la_qua_tang):
    sku = create_sku(upc=upc, ct_san_pham_id=ctsp_id, date_str=ngay_nhap, counter=counter)
    # 1 - (20/100) => 1 - 0.2
    thanh_tien = gia_nhap * so_luong * (1 - chiet_khau/100)
    ct_nhap_kho = ChiTietNhapKho(hoa_don_id=hoa_don_id, san_pham_id=san_pham_id, ctsp_id=ctsp_id, sku=sku, so_luong=so_luong, don_vi_tinh=don_vi_tinh, ke=ke, gia_nhap=gia_ban, gia_ban=gia_ban, chiet_khau=chiet_khau, thanh_tien=thanh_tien, la_qua_tang=la_qua_tang)

    db.session.add(ct_nhap_kho)
    print("ctsp_id:", ctsp_id)
    ctsp = ChiTietSanPham.query.get(ctsp_id)

    ctsp.so_luong = int(ctsp.so_luong) if ctsp.so_luong else 0 + int(so_luong) 
    
    db.session.add(ctsp)

    return thanh_tien