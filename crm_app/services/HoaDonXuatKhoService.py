from flask import make_response
from datetime import datetime
from crm_app.services.utils import validate_datetime, isExistId, create_sku
from crm_app.docs.containts import ERROR_CODES, get_error_response  
from crm_app.services.dbService import excute_select_data
from crm_app.models.Kho import Kho
from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietXuatKho import ChiTietXuatKho
from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app.models.HoaDonXuatKho import HoaDonXuatKho
from crm_app.models.KhachHang import KhachHang
from crm_app.models.NhanVien import NhanVien
from crm_app import db

def get_hoa_don_xuat_kho(filter, limit, page, sort, order):
    get_table = 'hoa_don_xuat_kho'
    get_attr = """
        khach_hang.id AS khach_hang_id, giao_hang.id AS nv_giao_hang_id, giao_hang.ho_ten AS nv_giao_hang, 
	    sale.id AS nv_sale_id, sale.ho_ten AS nv_sale, ngay_xuat, tong_tien, tra_truoc, (tong_tien - tra_truoc) AS con_lai, ghi_chu
    """

    query_join = """
        LEFT JOIN khach_hang ON khach_hang.id = hoa_don_xuat_kho.khach_hang_id
        LEFT JOIN nhan_vien giao_hang ON giao_hang.id = hoa_don_xuat_kho.nv_giao_hang_id
        LEFT JOIN nhan_vien sale ON sale.id = hoa_don_xuat_kho.nv_sale_id
    """
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)
    return get_error_response(ERROR_CODES.SUCCESS, result=response_data) 

def post_hoa_don_xuat_kho(khach_hang_id, nv_giao_hang_id, nv_sale_id, ngay_xuat, thanh_tien, tra_truoc, ghi_chu, ds_san_pham_xuat):
    print(ds_san_pham_xuat)
    # if validate_datetime(datetime_check=ngay_nhap) is False:
    #     return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 401)
    
    if isExistId(khach_hang_id, KhachHang) is False:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)
    
    isExist_nv_giao_hang = isExistId(nv_giao_hang_id, NhanVien)
    isExist_nv_sale = isExistId(nv_sale_id, NhanVien)
    if isExist_nv_giao_hang is False and isExist_nv_sale is False:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)
    
    if tra_truoc < 0 or tra_truoc > thanh_tien:
        return make_response(get_error_response(ERROR_CODES.PREPAID_INVALID), 401)
    
    new_hoa_don = HoaDonXuatKho(khach_hang_id=khach_hang_id  , nv_giao_hang_id=nv_giao_hang_id, nv_sale_id=nv_sale_id, ngay_xuat=ngay_xuat, thanh_tien=thanh_tien, tra_truoc=tra_truoc, ghi_chu=ghi_chu)

    db.session.add(new_hoa_don)
    db.session.flush()

    hoa_don_id = new_hoa_don.id
    total_money = 0
    if not ds_san_pham_xuat or len(ds_san_pham_xuat) == 0:
        return make_response(get_error_response(ERROR_CODES.NO_PRODUCT_SELECTED), 400)

    for item in ds_san_pham_xuat:
        gia_ban = item.get("gia_ban")
        chiet_khau = item.get("chiet_khau")
        if item.get("la_qua_tang") is True:
            gia_ban = 0
            chiet_khau = 0

        thanh_tien = add_ct_hoa_don_xuat(sku=item.get("sku"), hoa_don_id=hoa_don_id, san_pham_id=item.get("san_pham_id"), ctsp_id=item.get("ctsp_id"), so_luong=item.get("so_luong"), don_vi_tinh=item.get("don_vi_tinh"), gia_ban=gia_ban, chiet_khau=chiet_khau, la_qua_tang=item.get("la_qua_tang"))
        
        total_money = total_money + thanh_tien

    new_hoa_don.tong_tien = total_money

    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def add_ct_hoa_don_xuat(sku, hoa_don_id, san_pham_id, ctsp_id, so_luong, don_vi_tinh, gia_ban, chiet_khau, la_qua_tang):
    hd_nhap_kho = ChiTietNhapKho.query.filter_by(sku=sku).first()
    if hd_nhap_kho is None:
        return make_response(get_error_response(ERROR_CODES.NOT_FOUND), 401)
    
    if hd_nhap_kho.so_luong < so_luong:
        return make_response(get_error_response(ERROR_CODES.QUANTITY_NOT_ENOUGH), 401)
    if chiet_khau < 0 and chiet_khau > 100:
        return make_response(get_error_response(ERROR_CODES.CHIET_KHAU_INVALID), 401)
    # 1 - (20/100) => 1 - 0.2
    chiet_khau = chiet_khau if chiet_khau else 0 
    thanh_tien = gia_ban * so_luong * (1 - chiet_khau/100)

    ct_xuat_kho = ChiTietXuatKho(hoa_don_id=hoa_don_id, san_pham_id=san_pham_id, ctsp_id=ctsp_id, lo=sku,so_luong=so_luong, don_vi_tinh=don_vi_tinh, gia_ban=gia_ban, chiet_khau=chiet_khau, thanh_tien=thanh_tien, la_qua_tang=la_qua_tang)

    db.session.add(ct_xuat_kho)
    print("ctsp_id:", ctsp_id)
    ctsp = ChiTietSanPham.query.get(ctsp_id)

    ctsp.so_luong = (int(ctsp.so_luong) if ctsp.so_luong else 0) - int(so_luong) 
    
    

    db.session.add(ctsp)

    return thanh_tien