from flask import make_response
from datetime import datetime
from crm_app.services.utils import validate_datetime, isExistId, create_sku
from crm_app.services.utils import *
from crm_app.docs.containts import ERROR_CODES, get_error_response  
from crm_app.services.dbService import excute_select_data
from crm_app.models.NhaPhanPhoi import NhaPhanPhoi
from crm_app.models.Kho import Kho
from crm_app.models.HoaDonNhapKho import HoaDonNhapKho
from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app.models.SanPham import SanPham
from crm_app.models.TonKho import TonKho
from crm_app import db

def get_hoa_don_nhap_kho(filter, limit, page, sort, order):
    get_table = 'hoa_don_nhap_kho'
    get_attr = """
        so_hoa_don, ma_hoa_don, nha_phan_phoi.ten as nha_phan_phoi, nha_phan_phoi.id as nha_phan_phoi_id, 
        kho.ten as kho, kho.id as kho_id, ngay_nhap, 
        tong_tien, tra_truoc, con_lai, ghi_chu
    """
    query_join = """
        LEFT JOIN nha_phan_phoi ON hoa_don_nhap_kho.nha_phan_phoi_id = nha_phan_phoi.id
        LEFT JOIN kho ON hoa_don_nhap_kho.kho_id = kho.id
    """
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)

    return get_error_response(ERROR_CODES.SUCCESS, result=response_data) 

def post_hoa_don_nhap_kho(nha_phan_phoi_id, kho_id, ngay_nhap, tong_tien, tra_truoc, ghi_chu, ds_san_pham_nhap):
    print(ds_san_pham_nhap)
    # if validate_datetime(datetime_check=ngay_nhap) is False:
    #     return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 401)
    
    if not isExistId(nha_phan_phoi_id, NhaPhanPhoi):
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)

    if not isExistId(kho_id, Kho):
        return make_response(get_error_response(ERROR_CODES.KHO_NOT_FOUND), 401)
    
    error = validate_number(number=tra_truoc)
    if error:
        return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID), 401)
    
    error = validate_number(number=tong_tien)
    if error:
        return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID), 401)

    so_hoa_don = get_last_record_number_bill() + 1
    ma_hoa_don = create_bill_code(so_hoa_don, "HDN")
    new_hoa_don = HoaDonNhapKho(so_hoa_don=so_hoa_don, ma_hoa_don=ma_hoa_don,nha_phan_phoi_id=nha_phan_phoi_id, kho_id=kho_id, ngay_nhap=ngay_nhap, ghi_chu=ghi_chu)

    # try:
    db.session.add(new_hoa_don)
    db.session.flush()

    hoa_don_id = new_hoa_don.id
    counter = 0
    total_money = 0
    for item in ds_san_pham_nhap:
        gia_nhap = item.get("gia_nhap")
        gia_ban = item.get("gia_ban")
        chiet_khau = item.get("chiet_khau")
        
        upc = item.get("upc")    
        if item.get("la_qua_tang") is True:
            gia_nhap = 0
            gia_ban = 0
            chiet_khau = 0

        result = add_ct_hoa_don_nhap(upc=upc, ngay_nhap=ngay_nhap, counter=counter, hoa_don_id=hoa_don_id, san_pham_id=item.get("san_pham_id"), ctsp_id=item.get("ctsp_id"), so_luong=item.get("so_luong"), don_vi_tinh=item.get("don_vi_tinh"), ke=item.get("ke"), gia_nhap=gia_nhap, gia_ban=gia_ban, chiet_khau=chiet_khau, la_qua_tang=item.get("la_qua_tang"))

        if not isinstance(result, float):
            # raise ValueError()
            return result
        print('tổng tiền chi tiết sản phẩm', item.get("ctsp_id"), str(result))
        print('tổng tiền:', total_money)
        total_money = total_money + result
        counter += 1

    if tra_truoc > tong_tien:
        return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_PREPAID_GREATER_TOTAL_MONEY))
    print("total_money:", total_money)
    print("tong_tien:", tong_tien)
    if total_money != tong_tien:
        return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_TOTAL_MONEY_NOT_SAME), 401)

    con_lai = float(total_money) - float(tra_truoc)

    # ({"tong_tien": total_money, "tra_truoc": tra_truoc, "con_lai": con_lai})

    new_hoa_don.tong_tien = total_money
    new_hoa_don.tra_truoc = tra_truoc
    new_hoa_don.con_lai = con_lai

    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)
    # except Exception as e:
    #     db.session.rollback()
    #     return make_response(get_error_response(str(e)), 500)

def add_ct_hoa_don_nhap(upc, ngay_nhap, counter, hoa_don_id, san_pham_id, ctsp_id, so_luong, don_vi_tinh, ke, gia_nhap, gia_ban, chiet_khau, la_qua_tang):
    sku = create_sku(upc=upc, ct_san_pham_id=ctsp_id, date_str=ngay_nhap, counter=counter)
    
    if not isExistId(id=san_pham_id, model=SanPham):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND), 401)
    if not isExistId(id=ctsp_id, model=ChiTietSanPham):
        return make_response(get_error_response(ERROR_CODES.CTSP_NOT_FOUND), 401)

    for field_name, value in [("gia_nhap", gia_nhap), ("gia_nhap", gia_nhap), ("gia_ban", gia_ban), ("chiet_khau", chiet_khau)]:
        error = validate_number(number=value)
        if error:
            return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID, 401, f"Lỗi tại {field_name}"))

    # 1 - (20/100) => 1 - 0.2
    thanh_tien = gia_nhap * so_luong * (1 - chiet_khau/100)
    print(f"gia_nhap: {gia_nhap}")
    print(f"gia_ban: {gia_ban}")
    print(f"so_luong: {so_luong}")
    print(f"thành tiền: {thanh_tien}")
    ct_nhap_kho = ChiTietNhapKho(hoa_don_id=hoa_don_id, san_pham_id=san_pham_id, ctsp_id=ctsp_id, sku=sku, so_luong=so_luong, don_vi_tinh=don_vi_tinh, ke=ke, gia_nhap=gia_nhap, gia_ban=gia_ban, chiet_khau=chiet_khau, thanh_tien=thanh_tien, la_qua_tang=la_qua_tang)

    db.session.add(ct_nhap_kho)
    print("ctsp_id:", ctsp_id)
    ctsp = ChiTietSanPham.query.get(ctsp_id)

    ctsp.so_luong = (int(ctsp.so_luong) if ctsp.so_luong else 0) + int(so_luong)
    
    ton_kho = TonKho.query.filter_by(sku=sku).first()
    
    if ton_kho:
        ton_kho.so_luong_ton = int(ton_kho.so_luong_ton) + int(so_luong)
    else:
        new_ton_kho = TonKho(san_pham_id=san_pham_id, ctsp_id=ctsp_id, sku=sku, so_luong_ton = so_luong) 
        db.session.add(new_ton_kho)

    db.session.add(ctsp)

    return thanh_tien

def get_last_record_number_bill():
    curr_year = datetime.now().year

    last_record = (
        HoaDonNhapKho.query
        .filter(HoaDonNhapKho.created_at.between(f"{curr_year}-01-01", f"{curr_year}-12-31"))
        .order_by(HoaDonNhapKho.so_hoa_don.desc())
        .first()
    )
    print(last_record)
    if last_record:
        return int(last_record.so_hoa_don)
    else:
        return 1
    
def create_bill_code(number_bill, type:str):
    bill_code = f"{type}-{number_bill:06}"
    return bill_code
