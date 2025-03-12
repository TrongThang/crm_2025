from flask import make_response
from datetime import datetime
from crm_app.services.utils import validate_datetime, isExistId, create_sku, validate_number
from crm_app.docs.containts import ERROR_CODES, get_error_response  
from crm_app.services.dbService import excute_select_data
from crm_app.services.HoaDonNhapKhoService import create_bill_code, get_last_record_number_bill
from crm_app.models.Kho import Kho
from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietXuatKho import ChiTietXuatKho
from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app.models.SanPham import SanPham
from crm_app.models.HoaDonXuatKho import HoaDonXuatKho
from crm_app.models.KhachHang import KhachHang
from crm_app.models.NhanVien import NhanVien
from crm_app.models.TonKho import TonKho
from crm_app import db

def get_hoa_don_xuat_kho(filter, limit, page, sort, order):
    get_table = 'hoa_don_xuat_kho'
    get_attr = """
        khach_hang.id AS khach_hang_id, ho_hoa_don,  giao_hang.id AS nhan_vien_giao_hang_id, giao_hang.ho_ten AS nv_giao_hang, 
	    sale.id AS nv_sale_id, sale.ho_ten AS nv_sale, ngay_xuat, tong_tien, tra_truoc, (tong_tien - tra_truoc) AS con_lai, ghi_chu
    """

    query_join = """
        LEFT JOIN khach_hang ON khach_hang.id = hoa_don_xuat_kho.khach_hang_id
        LEFT JOIN nhan_vien giao_hang ON giao_hang.id = hoa_don_xuat_kho.nv_giao_hang_id
        LEFT JOIN nhan_vien sale ON sale.id = hoa_don_xuat_kho.nv_sale_id
    """
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)
    return get_error_response(ERROR_CODES.SUCCESS, result=response_data) 

def post_hoa_don_xuat_kho(khach_hang_id, nv_giao_hang_id, nv_sale_id, ngay_xuat, tong_tien, vat,thanh_tien, tra_truoc, tong_gia_nhap, loi_nhuan, ghi_chu, da_giao_hang, loai_chiet_khau, gia_tri_chiet_khau, ds_san_pham_xuat):
    print(ds_san_pham_xuat)
    # if validate_datetime(datetime_check=ngay_nhap) is False:
    #     return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 401)
    
    if isExistId(khach_hang_id, KhachHang) is False:
        return make_response(get_error_response(ERROR_CODES.KHACH_HANG_NOT_FOUND), 401)
    
    isExist_nv_giao_hang = isExistId(nv_giao_hang_id, NhanVien)
    print(isExist_nv_giao_hang)
    isExist_nv_sale = isExistId(nv_sale_id, NhanVien)
    print(isExist_nv_sale)
    if isExist_nv_giao_hang is False and isExist_nv_sale is False:
        return make_response(get_error_response(ERROR_CODES.NHAN_VIEN_NOT_FOUND), 401)
    
    # da_giao_hang = get_status_by_object(da_giao_hang)
    #     if not da_giao_hang:
    #         return make_response(get_error_response(ERROR_CODES.), 401)

    if tra_truoc < 0 or tra_truoc > thanh_tien:
        return make_response(get_error_response(ERROR_CODES.PREPAID_INVALID), 401)
    if validate_number(vat) is not None or vat > 100:
        return make_response(get_error_response(ERROR_CODES.CHIET_KHAU_INVALID), 401)
    
    if validate_number(tong_tien):
        return make_response(get_error_response(ERROR_CODES.TOTAL_MONEY_INVALID), 401)
    
    if not ds_san_pham_xuat:
        return make_response(get_error_response(ERROR_CODES.NO_PRODUCT_SELECTED), 400)

    so_hoa_don      = get_last_record_number_bill(model=HoaDonXuatKho) + 1
    ma_hoa_don      = create_bill_code(so_hoa_don, "HDX")

    #loai_chieu_khau: 1 - bán  / 0 - Tặng
    new_hoa_don     = HoaDonXuatKho(so_hoa_don=so_hoa_don, ma_hoa_don=ma_hoa_don,khach_hang_id=khach_hang_id, nhan_vien_giao_hang_id=nv_giao_hang_id, nhan_vien_sale_id=nv_sale_id, ngay_xuat=ngay_xuat, tong_tien=tong_tien, thanh_tien=thanh_tien, tra_truoc=tra_truoc, ghi_chu=ghi_chu, da_giao_hang=da_giao_hang, loai_chiet_khau=loai_chiet_khau, gia_tri_chiet_khau=gia_tri_chiet_khau)

    db.session.add(new_hoa_don)
    db.session.flush()

    hoa_don_id      = new_hoa_don.id

    total_cost      = 0 # Tổng giá nhập của sản phẩm
    total_money     = 0 # Tổng tiền - Là tổng các giá trị thành tiền sau khi thêm từng sản phẩm
    total_profit    = 0 # Lợi nhuận - Là tổng giá trị lợi nhuận của từng sản phẩm sau khi lấy giá bán trừ giá nhập
    print("hoàn thành lập hoá đơn")
    for item in ds_san_pham_xuat:
        result = add_ct_hoa_don_xuat(
            sku=item.get("sku"), hoa_don_id=hoa_don_id, san_pham_id=item.get("san_pham_id"), ctsp_id=item.get("ctsp_id"), so_luong_ban=item.get("so_luong_ban"), don_vi_tinh=item.get("don_vi_tinh"), gia_ban=item.get("gia_ban"), gia_nhap=item.get("gia_nhap"), thanh_tien=thanh_tien, chiet_khau=item.get("chiet_khau"), la_qua_tang=item.get("la_qua_tang")
        )
        if isinstance(result, dict):
            total_money       = total_money  + result.get("tong_tien")
            total_profit      = total_profit + result.get("loi_nhuan")
            total_cost        = total_cost   + result.get("tong_gia_nhap")
        else:
            return result
    
    print('tong_tien gửi về', new_hoa_don.tong_tien)
    print('tong_tien tính toán', total_money)
    if new_hoa_don.tong_tien != total_money:
        return make_response(get_error_response(ERROR_CODES.HOA_DON_XUAT_TOTAL_MONEY_NOT_SAME), 401)
    
    #Thành tiền - Số tiền thực tế mà khách hàng cần thanh toán - Là tổng tiền + với tiền thuế   
    total_amount = round(total_money * (1 + vat/100), 2)
    print('thành tiền gửi về:',total_amount, type(total_amount))
    print('thành tiền tính toán:', thanh_tien, type(thanh_tien))
    print('kết quả so sánh:', total_amount != thanh_tien)
    if total_amount != thanh_tien:
        print('khác')
        return make_response(get_error_response(ERROR_CODES.TOTAL_AMOUNT_INVALID), 401)
    
    print('tổng giá nhập gửi về:',total_cost, type(total_cost))
    print('tổng giá nhập tính toán:', tong_gia_nhap, type(tong_gia_nhap))
    if total_cost != tong_gia_nhap:
        return make_response(get_error_response(ERROR_CODES.TOTAL_COST_INVALID), 401)

    new_hoa_don.thanh_tien     = total_amount
    new_hoa_don.con_lai        = total_amount - tra_truoc 
    new_hoa_don.loi_nhuan      = total_profit
    new_hoa_don.tong_gia_nhap  = total_cost
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def add_ct_hoa_don_xuat(sku, hoa_don_id, san_pham_id, ctsp_id, so_luong_ban, don_vi_tinh, gia_ban, gia_nhap, thanh_tien, chiet_khau, la_qua_tang):
    if not isExistId(id = san_pham_id,  model = SanPham):
        return make_response(get_error_response(ERROR_CODES.PRODUCT_NOT_FOUND), 401)
    if not isExistId(id = ctsp_id, model = ChiTietSanPham):
        return make_response(get_error_response(ERROR_CODES.CTSP_NOT_FOUND), 401)


    hd_nhap_kho = ChiTietNhapKho.query.filter_by(sku=sku).first()
    if hd_nhap_kho is None:
        return make_response(get_error_response(ERROR_CODES.NOT_FOUND), 401)
    
    print(f'số lưognj còn trong kho lô hàng {sku}:',hd_nhap_kho.so_luong)
    print(f'số lưognj bán lô hàng {sku}:', so_luong_ban)
    if int(hd_nhap_kho.so_luong) < so_luong_ban:
        return make_response(get_error_response(ERROR_CODES.QUANTITY_NOT_ENOUGH), 401)
    
    if chiet_khau < 0 and chiet_khau > 100:
        return make_response(get_error_response(ERROR_CODES.CHIET_KHAU_INVALID), 401)

    if not isinstance(gia_ban, (int, float)) or gia_ban < 0:
        return make_response(get_error_response(ERROR_CODES.INVALID_PRICE), 401)
    
    if not isinstance(gia_nhap, (int, float)) or gia_nhap < 0:
        return make_response(get_error_response(ERROR_CODES.INVALID_COST), 401)
    
    if la_qua_tang in [True, False, 0, 1]:
        if la_qua_tang in [True, 1]:
            gia_ban     = 0
            chiet_khau  = 0
    else:
        return make_response(get_error_response(ERROR_CODES.INVALID_GIFT_FLAG), 401)

    # 1 - (20/100) => 1 - 0.2
    tong_tien       = gia_ban * so_luong_ban
    thanh_tien      = gia_ban * so_luong_ban * (1 - chiet_khau/100)
    total_cost      = gia_nhap * so_luong_ban
    loi_nhuan       = thanh_tien - total_cost
    print('loi_nhuan:', loi_nhuan)
    ct_xuat_kho     = ChiTietXuatKho(hoa_don_id=hoa_don_id, san_pham_id=san_pham_id, ctsp_id=ctsp_id, sku=sku,so_luong_ban=so_luong_ban, don_vi_tinh=don_vi_tinh, gia_ban=gia_ban, gia_nhap=gia_nhap, chiet_khau=chiet_khau, thanh_tien=thanh_tien, loi_nhuan=loi_nhuan, la_qua_tang=la_qua_tang)

    db.session.add(ct_xuat_kho)
    print("ctsp_id:", ctsp_id)
    ctsp            = ChiTietSanPham.query.get(ctsp_id)
    ton_kho         = TonKho.query.filter_by(sku=sku).first()


    ctsp.so_luong   = int(ctsp.so_luong)         - int(so_luong_ban)
    ton_kho.so_luong= int(ton_kho.so_luong_ton)  - int(so_luong_ban) 

    db.session.add(ctsp)

    return {"tong_tien":tong_tien, "thanh_tien":thanh_tien, "loi_nhuan":loi_nhuan, "tong_gia_nhap":total_cost}