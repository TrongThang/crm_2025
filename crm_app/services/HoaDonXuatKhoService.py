from flask import make_response
from datetime import datetime
from crm_app.services.utils import convert_datetime, isExistId, create_sku, validate_number
from crm_app.docs.containts import ERROR_CODES, get_error_response  
from crm_app.services.dbService import excute_select_data
from crm_app.services.HoaDonNhapKhoService import create_bill_code, get_last_record_number_bill
from crm_app.models.Kho import Kho
from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietXuatKho import ChiTietXuatKho
from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app.models.SanPham import SanPham
from crm_app.models.HoaDonXuatKho import HoaDonXuatKho
from crm_app.models.HoaDonNhapKho import HoaDonNhapKho
from crm_app.models.KhachHang import KhachHang
from crm_app.models.NhanVien import NhanVien
from crm_app.models.TonKho import TonKho
from crm_app import db
from collections import defaultdict
from sqlalchemy import text
import math

def config_data_response(raw_data):
    # Dictionary để nhóm hóa đơn nhập kho
    grouped_data = defaultdict(lambda: {
        "hoa_don_id": None,
        "so_hoa_don": None,
        "ma_hoa_don": None,
        "khach_hang_id": None,
        "khach_hang": None,
        "nhan_vien_giao_hang_id": None,
        "nhan_vien_giao_hang": None,
        "nhan_vien_sale_id": None,
        "nhan_vien_sale": None,
        "ngay_xuat": None,
        "tong_tien": None,
        "tra_truoc": None,
        "con_lai": None,
        "ghi_chu": None,
        "ds_san_pham_xuat": []
    })
    # Nhóm dữ liệu
    for row in raw_data:
        hoa_don_id = row["ID"]
        
        # Nếu hóa đơn chưa được thêm vào dictionary, thêm thông tin chung
        if grouped_data[hoa_don_id]["hoa_don_id"] is None:
            grouped_data[hoa_don_id].update({
                "ID": hoa_don_id,
                "so_hoa_don": row["so_hoa_don"],
                "ma_hoa_don": row["ma_hoa_don"],
                "khach_hang_id": row["khach_hang_id"],
                "khach_hang": row["khach_hang"],
                "nhan_vien_giao_hang_id": row["nhan_vien_giao_hang_id"],
                "nhan_vien_giao_hang": row["nhan_vien_giao_hang"],
                "nhan_vien_sale_id": row["nhan_vien_sale_id"],
                "nhan_vien_sale": row["nhan_vien_sale"],
                "ngay_xuat": row["ngay_xuat"],
                "vat": row["vat"],
                "tong_tien": row["tong_tien"],
                "tra_truoc": row["tra_truoc"],
                "con_lai": row["con_lai"],
                "ghi_chu": row["ghi_chu"],
                "da_giao_hang": row["da_giao_hang"],
                "khoa_don": row["khoa_don"],
                "loai_chiet_khau": row["loai_chiet_khau"],
                "gia_tri_chiet_khau": row["gia_tri_chiet_khau"],
                "CreatedAt": row["CreatedAt"],
                "UpdatedAt": row["UpdatedAt"],
                "DeletedAt": row["DeletedAt"],
            })
        
        # Thêm chi tiết hóa đơn vào danh sách
        grouped_data[hoa_don_id]["ds_san_pham_xuat"].append({
            "ID": row["cthd_xuat_kho_id"],
            "upc": row["upc"],
            "san_pham_id": row["san_pham_id"],
            "ctsp_id": row["ctsp_id"],
            "ctsp_ten": row["ctsp_ten"],
            "san_pham_ten": row["san_pham_ten"],
            "sku": row["sku"],
            "sku_xuat": row["sku_xuat"],
            # "han_su_dung": row["han_su_dung"],
            "so_luong_ban": row["so_luong_ban"],
            "don_vi_tinh": row["don_vi_tinh"],
            "gia_nhap": row["gia_nhap"],
            "gia_ban": row["gia_ban"],
            "thanh_tien": row["thanh_tien"],
            "chiet_khau": row["chiet_khau"],
            "la_qua_tang": row["la_qua_tang"],
        })

    return list(grouped_data.values())

def get_hoa_don_xuat_kho(filter, limit, page, sort, order):
    get_table = 'hoa_don_xuat_kho'
    get_attr = """
        khach_hang.id AS khach_hang_id, khach_hang.ho_ten AS khach_hang, so_hoa_don, ma_hoa_don,giao_hang.id AS nhan_vien_giao_hang_id, giao_hang.ho_ten AS nhan_vien_giao_hang, sale.id AS nhan_vien_sale_id, sale.ho_ten AS nhan_vien_sale, ngay_xuat, tong_tien, tra_truoc, (tong_tien - tra_truoc) AS con_lai, ghi_chu, da_giao_hang, khoa_don,loai_chiet_khau, gia_tri_chiet_khau, hoa_don_xuat_kho.vat,
        
        chi_tiet_hoa_don_xuat_kho.id as cthd_xuat_kho_id, san_pham.upc AS upc, san_pham.id as san_pham_id, san_pham.ten as san_pham_ten, chi_tiet_san_pham.id AS ctsp_id, chi_tiet_san_pham.ten_phan_loai as ctsp_ten, sku_xuat,
        chi_tiet_hoa_don_xuat_kho.don_vi_tinh, chi_tiet_hoa_don_xuat_kho.so_luong_ban, chi_tiet_hoa_don_xuat_kho.gia_ban,  chi_tiet_hoa_don_xuat_kho.gia_nhap, chi_tiet_hoa_don_xuat_kho.chiet_khau, chi_tiet_hoa_don_xuat_kho.thanh_tien, chi_tiet_hoa_don_xuat_kho.la_qua_tang, chi_tiet_hoa_don_xuat_kho.sku
    """

    query_join = """
        LEFT JOIN chi_tiet_hoa_don_xuat_kho ON chi_tiet_hoa_don_xuat_kho.hoa_don_id = hoa_don_xuat_kho.id
        LEFT JOIN nhan_vien giao_hang ON giao_hang.id = hoa_don_xuat_kho.nhan_vien_giao_hang_id
        LEFT JOIN nhan_vien sale ON sale.id = hoa_don_xuat_kho.nhan_vien_sale_id
        LEFT JOIN khach_hang ON khach_hang.id = hoa_don_xuat_kho.khach_hang_id
        LEFT JOIN san_pham ON san_pham.id = chi_tiet_hoa_don_xuat_kho.san_pham_id
        LEFT JOIN chi_tiet_san_pham ON chi_tiet_san_pham.id = chi_tiet_hoa_don_xuat_kho.ctsp_id
    """
    
    raw_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)

    query_total = text(f" SELECT COUNT(*) FROM hoa_don_xuat_kho WHERE hoa_don_xuat_kho.deleted_at IS NULL LIMIT {limit or 0}")
    total_count = db.session.execute(query_total).scalar()
    total_page = math.ceil(total_count / int(limit)) if limit else 1

    response_data = {
        "data": config_data_response(raw_data.get("data")), 
        "total_page": total_page
    }

    return get_error_response(ERROR_CODES.SUCCESS, result=response_data) 

def get_counter_export_product_in_day(ngay_xuat, ctsp_id):
    query = text(f"""
                SELECT COUNT(id)
                FROM hoa_don_xuat_kho
                WHERE DATE(ngay_xuat) = :ngay_xuat
                AND id IN  (SELECT hoa_don_xuat_kho.id
                            FROM hoa_don_xuat_kho
                            LEFT JOIN chi_tiet_hoa_don_xuat_kho ON chi_tiet_hoa_don_xuat_kho.hoa_don_id = hoa_don_xuat_kho.id
                            AND chi_tiet_hoa_don_xuat_kho.ctsp_id =:ctsp_id
                        )
                FOR UPDATE
                """)    
    count = db.session.execute(query, {"ngay_xuat": ngay_xuat, "ctsp_id": ctsp_id}).scalar()
    return count

def post_hoa_don_xuat_kho(khach_hang_id, nv_giao_hang_id, nv_sale_id, ngay_xuat, tong_tien, vat,thanh_tien, tra_truoc, tong_gia_nhap, loi_nhuan, ghi_chu, da_giao_hang, loai_chiet_khau, gia_tri_chiet_khau, ds_san_pham_xuat):
    try:
        if isExistId(khach_hang_id, KhachHang) is False:
            return make_response(get_error_response(ERROR_CODES.KHACH_HANG_NOT_FOUND), 500)
        ngay_xuat = convert_datetime(ngay_xuat)
        if ngay_xuat is False:
            return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 500)
        
        isExist_nv_giao_hang = isExistId(nv_giao_hang_id, NhanVien)
        print(isExist_nv_giao_hang)
        isExist_nv_sale = isExistId(nv_sale_id, NhanVien)
        print(isExist_nv_sale)
        if isExist_nv_giao_hang is False and isExist_nv_sale is False:
            return make_response(get_error_response(ERROR_CODES.NHAN_VIEN_NOT_FOUND), 500)
        
        # da_giao_hang = get_status_by_object(da_giao_hang)
        #     if not da_giao_hang:
        #         return make_response(get_error_response(ERROR_CODES.), 500)
        if tra_truoc < 0 or tra_truoc > thanh_tien:
            return make_response(get_error_response(ERROR_CODES.PREPAID_INVALID), 500)
        if validate_number(vat) is not None or vat > 100:
            return make_response(get_error_response(ERROR_CODES.CHIET_KHAU_INVALID), 500)
        
        if validate_number(tong_tien):
            return make_response(get_error_response(ERROR_CODES.TOTAL_MONEY_INVALID), 500)
        
        if not ds_san_pham_xuat:
            return make_response(get_error_response(ERROR_CODES.NO_PRODUCT_SELECTED), 400)

        so_hoa_don      = get_last_record_number_bill(model=HoaDonXuatKho) + 1
        ma_hoa_don      = create_bill_code(so_hoa_don, "HDX")

        #loai_chieu_khau: 1 - bán  / 0 - Tặng
        new_hoa_don     = HoaDonXuatKho(so_hoa_don=so_hoa_don, ma_hoa_don=ma_hoa_don,khach_hang_id=khach_hang_id, nhan_vien_giao_hang_id=nv_giao_hang_id, nhan_vien_sale_id=nv_sale_id, ngay_xuat=ngay_xuat, tong_tien=tong_tien, thanh_tien=thanh_tien, tra_truoc=tra_truoc, ghi_chu=ghi_chu, da_giao_hang=da_giao_hang, loai_chiet_khau=loai_chiet_khau, gia_tri_chiet_khau=gia_tri_chiet_khau)
        print('thành tiền lúc tạo hoá đơn:',thanh_tien)
        db.session.add(new_hoa_don)
        db.session.flush()

        hoa_don_id      = new_hoa_don.id

        total_cost      = 0 # Tổng giá nhập của sản phẩm
        total_money     = 0 # Tổng tiền - Là tổng các giá trị thành tiền sau khi thêm từng sản phẩm
        total_profit    = 0 # Lợi nhuận - Là tổng giá trị lợi nhuận của từng sản phẩm sau khi lấy giá bán trừ giá nhập
        total_amount    = 0
        print("hoàn thành lập hoá đơn")
        for item in ds_san_pham_xuat:
            result = add_ct_hoa_don_xuat(
                ds_sku=item.get("ds_sku"), ngay_xuat=ngay_xuat, hoa_don_id=hoa_don_id, upc=item.get("upc"),san_pham_id=item.get("san_pham_id"), ctsp_id=item.get("ctsp_id"), so_luong_ban=item.get("so_luong_ban"), don_vi_tinh=item.get("don_vi_tinh"), gia_ban=item.get("gia_ban"), gia_nhap=item.get("gia_nhap"), thanh_tien=thanh_tien, chiet_khau=item.get("chiet_khau"), la_qua_tang=item.get("la_qua_tang")
            )
            if isinstance(result, dict):
                total_money       = total_money  + result.get("thanh_tien")
                # total_amount      = total_amount + result.get("thanh_tien")
                total_profit      = total_profit + result.get("loi_nhuan")
                total_cost        = total_cost   + result.get("tong_gia_nhap")
            else:
                return result
        
        print("total_amount:", new_hoa_don.thanh_tien)
        if new_hoa_don.tong_tien != total_money:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_XUAT_TOTAL_MONEY_NOT_SAME), 500)
        
        #Thành tiền - Số tiền thực tế mà khách hàng cần thanh toán - Là tổng tiền + với tiền thuế   
        print("total_amount trước:", total_amount)
        total_amount = round(total_money * (1 + vat/100), 2)
        print("total_amount:", total_amount)

        if total_amount != thanh_tien:
            return make_response(get_error_response(ERROR_CODES.TOTAL_AMOUNT_INVALID), 500)
        print("total_cost:", total_cost)
        # if total_cost != tong_gia_nhap:
        #     return make_response(get_error_response(ERROR_CODES.TOTAL_COST_INVALID), 500)

        new_hoa_don.thanh_tien     = total_amount
        new_hoa_don.con_lai        = total_amount - tra_truoc 
        new_hoa_don.loi_nhuan      = total_profit
        new_hoa_don.tong_gia_nhap  = total_cost
        db.session.commit()

        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(str(e), 500)

def add_ct_hoa_don_xuat(ngay_xuat, ds_sku, hoa_don_id, upc, san_pham_id, ctsp_id, so_luong_ban, don_vi_tinh, gia_ban, gia_nhap, thanh_tien, chiet_khau, la_qua_tang):
    if not isExistId(id = san_pham_id,  model = SanPham):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND), 500)
    if not isExistId(id = ctsp_id, model = ChiTietSanPham):
        return make_response(get_error_response(ERROR_CODES.CTSP_NOT_FOUND), 500)


    # hd_nhap_kho = ChiTietNhapKho.query.get(hoa_don_id)
    # if hd_nhap_kho is None:
    #     return make_response(get_error_response(ERROR_CODES.NOT_FOUND), 500)
    
    if chiet_khau < 0 and chiet_khau > 100:
        return make_response(get_error_response(ERROR_CODES.CHIET_KHAU_INVALID), 500)

    if not isinstance(gia_ban, (int, float)) or gia_ban < 0:
        return make_response(get_error_response(ERROR_CODES.INVALID_PRICE), 500)
    
    # print(gia_nhap)
    # if not isinstance(gia_nhap, (int, float)) or gia_nhap < 0:
    #     return make_response(get_error_response(ERROR_CODES.INVALID_COST), 500)
    print('kiểm tra la quà tặng')
    if la_qua_tang in [True, False, 0, 1]:

        if la_qua_tang in [True, 1]:
            gia_ban     = 0
            chiet_khau  = 0
    else:
        return make_response(get_error_response(ERROR_CODES.INVALID_GIFT_FLAG), 500)
    
    couter_export_by_ctsp = get_counter_export_product_in_day(ngay_xuat=ngay_xuat, ctsp_id=ctsp_id)
    sku_xuat = create_sku(upc = upc, ct_san_pham_id = ctsp_id, date_str=ngay_xuat, counter_detail_product_in_date=couter_export_by_ctsp)
    # 1 - (20/100) => 1 - 0.2
    tong_tien             = gia_ban * so_luong_ban
    thanh_tien            = gia_ban * so_luong_ban * (1 - chiet_khau/100)
    print("thanh_tien:", thanh_tien)
    total_cost            = 0
    so_luong_ban_caculate = 0
    
    for item_sku in ds_sku:
        sku = item_sku.get("sku")
        ton_kho = TonKho.query.filter_by(sku = sku, deleted_at = None).first()
        so_luong_ban_sku      = item_sku.get("so_luong_ban")
        print("sku:", sku)
        print("so_luong_ban_sku:", so_luong_ban_sku)

        
        if not ton_kho:
            return make_response(get_error_response(ERROR_CODES.KHO_NOT_EXISTED_SKU, field_error=sku), 500)
        
        if so_luong_ban_sku > int(ton_kho.so_luong_ton):
            return make_response(get_error_response(ERROR_CODES.KHO_NOT_QUANTITY_FOR_SALE), 500) 
        
        ctnk = ChiTietNhapKho.query.filter_by(sku=sku, deleted_at = None).first()
        gia_nhap = ctnk.gia_nhap if ctnk.gia_nhap else 0
        print(not gia_nhap)
        if gia_nhap < 0:
            return make_response(get_error_response(ERROR_CODES.INVALID_COST), 500)
        
        so_luong_ban_caculate = so_luong_ban_caculate + so_luong_ban_sku
        thanh_tien_sku        = gia_ban * so_luong_ban_sku * (1 - chiet_khau/100)
        print("thanh_tien_sku:",thanh_tien_sku)
        cost_sku              = gia_nhap * so_luong_ban_sku
        total_cost            += cost_sku
        loi_nhuan_sku         = thanh_tien_sku - cost_sku
        # thanh_tien            += thanh_tien_sku

        ct_xuat_kho           = ChiTietXuatKho(hoa_don_id=hoa_don_id, san_pham_id=san_pham_id, ctsp_id=ctsp_id,sku_xuat=sku_xuat, sku=sku,so_luong_ban=so_luong_ban_sku, don_vi_tinh=don_vi_tinh, gia_ban=gia_ban, gia_nhap=gia_nhap, chiet_khau=chiet_khau, thanh_tien=thanh_tien_sku, loi_nhuan=loi_nhuan_sku, la_qua_tang=la_qua_tang)
        db.session.add(ct_xuat_kho)

    loi_nhuan = thanh_tien - total_cost
    print('so_luong_ban_caculate', so_luong_ban_caculate)
    print('so_luong_ban', so_luong_ban)
    if so_luong_ban_caculate != so_luong_ban:
        return make_response(get_error_response(ERROR_CODES.HOA_DON_XUAT_SO_LUONG_BAN_NOT_SAME), 500)

    
    ctsp            = ChiTietSanPham.query.get(ctsp_id)
    ton_kho         = TonKho.query.filter_by(sku=sku).first()

    ctsp.so_luong   = int(ctsp.so_luong)         - int(so_luong_ban)
    print('so luong ton:', ton_kho.so_luong_ton)
    print('so_luong_ban:', so_luong_ban)
    ton_kho.so_luong_ton = int(ton_kho.so_luong_ton)  - int(so_luong_ban) 
    if ton_kho.so_luong_ton <= 0:
        ton_kho.soft_delete()
    return {"tong_tien":tong_tien, "thanh_tien":thanh_tien, "loi_nhuan":loi_nhuan, "tong_gia_nhap":total_cost}

def put_hoa_don_xuat_kho(hoa_don_id, khach_hang_id, nv_giao_hang_id, nv_sale_id, ngay_xuat, vat, tra_truoc, ghi_chu, da_giao_hang, loai_chiet_khau, gia_tri_chiet_khau, khoa_don):
    try:
        hoa_don = HoaDonXuatKho.query.get(hoa_don_id)
        if not hoa_don:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_XUAT_NOT_FOUND), 500)
        ngay_xuat = convert_datetime(ngay_xuat)
        if ngay_xuat is False:
            return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 500)
        
        if isExistId(khach_hang_id, KhachHang) is False:
            return make_response(get_error_response(ERROR_CODES.KHACH_HANG_NOT_FOUND), 500)
        
        isExist_nv_giao_hang = isExistId(nv_giao_hang_id, NhanVien)
        
        isExist_nv_sale = isExistId(nv_sale_id, NhanVien)
        
        if isExist_nv_giao_hang is False and isExist_nv_sale is False:
            return make_response(get_error_response(ERROR_CODES.NHAN_VIEN_NOT_FOUND), 500)
        
        if not da_giao_hang in [0, 1]:
            return make_response(get_error_response(ERROR_CODES.DELIVERED_STATUS_INVALID), 500)

        if tra_truoc < 0 or tra_truoc > hoa_don.thanh_tien:
            return make_response(get_error_response(ERROR_CODES.PREPAID_INVALID), 500)
        if validate_number(vat) is not None or vat > 100:
            return make_response(get_error_response(ERROR_CODES.CHIET_KHAU_INVALID), 500)
        
        #loai_chieu_khau: 1 - bán  / 0 - Tặng
        hoa_don.khach_hang_id           = khach_hang_id
        hoa_don.nhan_vien_giao_hang_id  = nv_giao_hang_id
        hoa_don.nhan_vien_sale_id       = nv_sale_id
        hoa_don.ngay_xuat               = ngay_xuat
        hoa_don.ghi_chu                 = ghi_chu
        hoa_don.da_giao_hang            = da_giao_hang
        hoa_don.loai_chiet_khau         = loai_chiet_khau
        hoa_don.gia_tri_chiet_khau      = gia_tri_chiet_khau
        hoa_don.khoa_don                = khoa_don 
        
        if hoa_don.vat != vat:
            hoa_don.vat                 = vat
            hoa_don.thanh_tien          = hoa_don.thanh_tien * (1 - hoa_don.vat/100)
        
        if hoa_don.tra_truoc != tra_truoc:
            hoa_don.tra_truoc           = tra_truoc
        hoa_don.con_lai                 = hoa_don.thanh_tien - hoa_don.tra_truoc
            

        print("hoàn thành chỉnh sửa hoá đơn")   
        db.session.commit()

        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(str(e), 500)
    
def patch_lock(hoa_don_id, khoa_don):
    try:
        hoa_don = HoaDonXuatKho.query.get(hoa_don_id)
        if not hoa_don:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_NOT_FOUND), 404)
        if khoa_don not in ["lock", "open"]:
            return make_response(get_error_response(ERROR_CODES.LOCK_STATUS_INVALID))
        khoa_don = True if khoa_don == "lock" else False
        print("hoa_don:",hoa_don)
        print("khoa_don:",khoa_don)
        hoa_don.khoa_don = khoa_don
        db.session.commit()
        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(get_error_response(ERROR_CODES.SERVER_EROR), 500)    

def tra_no_khach_hang(hoa_don_id, tien_tra):
    hoa_don = HoaDonXuatKho.query.get(hoa_don_id)

    if not hoa_don:
        return make_response(get_error_response(ERROR_CODES.HOA_DON_XUAT_NOT_STATUS), 500)
    
    con_lai = hoa_don.con_lai
    error = validate_number(number=tien_tra, start=0, end = con_lai)
    if not error:
        return error
    
    hoa_don.con_lai = con_lai - tien_tra
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def tra_hang(hoa_don_id, ds_san_pham_tra):
    try:
        hoa_don = HoaDonXuatKho.query.get(hoa_don_id)
        if not hoa_don:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_XUAT_NOT_FOUND), 500)

        for san_pham_tra in ds_san_pham_tra:
            id = san_pham_tra.get("cthd_xuat_kho_id")
            so_luong_tra = san_pham_tra.get("so_luong_tra")
            sku = san_pham_tra.get("sku")

            ct_hoa_don_xuat = ChiTietXuatKho.query.get(id)
            if not ct_hoa_don_xuat:
                return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND), 500)
            
            if validate_number(so_luong_tra, 1):
                return make_response(get_error_response(ERROR_CODES.SO_LUONG_TRA_GREATED_THAN_ZERO), 500)
            
            if so_luong_tra > ct_hoa_don_xuat.so_luong_ban:
                return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_SL_TRA_GREATED_THAN_SO_LUONG_SALE), 500)
            
            ton_kho = TonKho.query.filter_by(sku=sku).first()

            if not ton_kho:
                return make_response(get_error_response(ERROR_CODES.KHO_NOT_EXISTED_SKU), 500)
            
            if ton_kho == 0 and ton_kho.deleted_at:
                ton_kho.restore()
            
            ton_kho.so_luong_ton         += so_luong_tra
            ct_hoa_don_xuat.so_luong_ban -= so_luong_tra

        db.session.commit()
        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(str(e), 500)