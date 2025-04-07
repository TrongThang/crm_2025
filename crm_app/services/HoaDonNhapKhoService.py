from flask import make_response, Response
from datetime import datetime
from crm_app.services.utils import convert_datetime, isExistId, create_sku
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
from collections import defaultdict
import math
from crm_app.helpers.kafka import producer

def config_data_response(raw_data):
    # Dictionary để nhóm hóa đơn nhập kho
    grouped_data = defaultdict(lambda: {
        "hoa_don_id": None,
        "so_hoa_don": None,
        "ma_hoa_don": None,
        "nha_phan_phoi": None,
        "nha_phan_phoi_id": None,
        "kho": None,
        "kho_id": None,
        "ngay_nhap": None,
        "tong_tien": None,
        "tra_truoc": None,
        "con_lai": None,
        "ghi_chu": None,
        "ds_san_pham_nhap": []
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
                "nha_phan_phoi": row["nha_phan_phoi"],
                "nha_phan_phoi_id": row["nha_phan_phoi_id"],
                "kho": row["kho"],
                "kho_id": row["kho_id"],
                "ngay_nhap": row["ngay_nhap"],
                "tong_tien": row["tong_tien"],
                "tra_truoc": row["tra_truoc"],
                "con_lai": row["con_lai"],
                "ghi_chu": row["ghi_chu"],
                "khoa_don": row["khoa_don"],
                "CreatedAt": row["CreatedAt"],
                "UpdatedAt": row["UpdatedAt"],
                "DeletedAt": row["DeletedAt"],
            })
        
        # Thêm chi tiết hóa đơn vào danh sách
        grouped_data[hoa_don_id]["ds_san_pham_nhap"].append({
            "ID": row["cthd_nhap_kho_id"],
            "upc": row["upc"],
            "san_pham_id": row["san_pham_id"],
            "ctsp_id": row["ctsp_id"],
            "ctsp_ten": row["ctsp_ten"],
            "san_pham_ten": row["san_pham_ten"],
            "sku": row["sku"],
            "han_su_dung": row["han_su_dung"],
            "so_luong": row["so_luong"],
            "don_vi_tinh": row["don_vi_tinh"],
            "ke": row["ke"],
            "gia_nhap": row["gia_nhap"],
            "gia_ban": row["gia_ban"],
            "thanh_tien": row["thanh_tien"],
            "chiet_khau": row["chiet_khau"],
            "la_qua_tang": row["la_qua_tang"],
        })

    return list(grouped_data.values())

def get_hoa_don_nhap_kho(filter, limit, page, sort, order):
    get_table = 'hoa_don_nhap_kho'
    get_attr = """
        so_hoa_don, ma_hoa_don, nha_phan_phoi.ten as nha_phan_phoi, nha_phan_phoi.id as nha_phan_phoi_id, 
        kho.ten as kho, kho.id as kho_id, ngay_nhap, khoa_don,
        tong_tien, tra_truoc, con_lai, ghi_chu,
        chi_tiet_hoa_don_nhap_kho.id AS cthd_nhap_kho_id, chi_tiet_hoa_don_nhap_kho.san_pham_id, chi_tiet_hoa_don_nhap_kho.ctsp_id, chi_tiet_hoa_don_nhap_kho.sku, chi_tiet_hoa_don_nhap_kho.han_su_dung , chi_tiet_hoa_don_nhap_kho.so_luong, chi_tiet_hoa_don_nhap_kho.don_vi_tinh, chi_tiet_hoa_don_nhap_kho.ke, chi_tiet_hoa_don_nhap_kho.gia_nhap, chi_tiet_hoa_don_nhap_kho.gia_ban, chi_tiet_hoa_don_nhap_kho.thanh_tien, chi_tiet_hoa_don_nhap_kho.chiet_khau, chi_tiet_san_pham.ten_phan_loai as ctsp_ten, chi_tiet_hoa_don_nhap_kho.la_qua_tang, san_pham.ten AS san_pham_ten, san_pham.upc
    """
    query_join = """
        LEFT JOIN nha_phan_phoi ON hoa_don_nhap_kho.nha_phan_phoi_id = nha_phan_phoi.id
        LEFT JOIN kho ON hoa_don_nhap_kho.kho_id = kho.id
        LEFT JOIN chi_tiet_hoa_don_nhap_kho ON chi_tiet_hoa_don_nhap_kho.hoa_don_id = hoa_don_nhap_kho.id
        LEFT JOIN chi_tiet_san_pham ON chi_tiet_san_pham.id = chi_tiet_hoa_don_nhap_kho.ctsp_id
        LEFT JOIN san_pham ON san_pham.id = chi_tiet_san_pham.san_pham_id
    """
    
    raw_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)

    query_total = text(f" SELECT COUNT(*) FROM hoa_don_nhap_kho WHERE hoa_don_nhap_kho.deleted_at IS NULL LIMIT {limit or 0}")
    total_count = db.session.execute(query_total).scalar()
    total_page = math.ceil(total_count / int(limit)) if limit else 1

    response_data = {
        "data": config_data_response(raw_data.get("data")), 
        "total_page": total_page
    }

    return get_error_response(ERROR_CODES.SUCCESS, result=response_data) 

def post_hoa_don_nhap_kho(nha_phan_phoi_id, kho_id, ngay_nhap, tong_tien, tra_truoc, ghi_chu, ds_san_pham_nhap):
    print(ds_san_pham_nhap)
    ngay_nhap = convert_datetime(ngay_nhap)
    if ngay_nhap is False:
        return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 400)
    
    if not isExistId(nha_phan_phoi_id, NhaPhanPhoi):
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 400)

    if not isExistId(kho_id, Kho):
        return make_response(get_error_response(ERROR_CODES.KHO_NOT_FOUND), 400)
    
    error = validate_number(number=tra_truoc)
    if error:
        return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID), 400)
    
    error = validate_number(number=tong_tien)
    if error:
        return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID), 400)
    
    try:
        db.session.rollback()

        db.session.begin()

        so_hoa_don  = get_last_record_number_bill(model=HoaDonNhapKho) + 1
        ma_hoa_don  = create_bill_code(so_hoa_don, "HDN")
        new_hoa_don = HoaDonNhapKho(so_hoa_don=so_hoa_don, ma_hoa_don=ma_hoa_don,nha_phan_phoi_id=nha_phan_phoi_id, kho_id=kho_id, ngay_nhap=ngay_nhap, ghi_chu=ghi_chu)
    
        # try:
        db.session.add(new_hoa_don)
        db.session.flush()

        hoa_don_id  = new_hoa_don.id
        counter     = 0
        total_money = 0
        profit      = 0
        for item in ds_san_pham_nhap:
            gia_nhap    = item.get("gia_nhap")
            gia_ban     = item.get("gia_ban")
            chiet_khau  = item.get("chiet_khau")
            
            upc = item.get("upc")    
            if item.get("la_qua_tang") is True:
                gia_nhap    = 0
                gia_ban     = 0
                chiet_khau  = 0
            result = add_ct_hoa_don_nhap(upc=upc, ngay_nhap=ngay_nhap, counter=counter, hoa_don_id=hoa_don_id, san_pham_id=item.get("san_pham_id"), ctsp_id=item.get("ctsp_id"), so_luong=item.get("so_luong"), don_vi_tinh=item.get("don_vi_tinh"), ke=item.get("ke"), gia_nhap=gia_nhap, gia_ban=gia_ban, chiet_khau=chiet_khau, thanh_tien=item.get("thanh_tien"),la_qua_tang=item.get("la_qua_tang"))

            if isinstance(result, Response):
                return result
            total_money = total_money + result  
            counter     += 1
            
            event_data = {
                "hoa_don_id": hoa_don_id,
                "san_pham_id": item.get("san_pham_id"),
                "so_luong": item.get("so_luong"),
                "gia_nhap": item.get("gia_nhap"),
                "gia_ban": item.get("gia_ban"),
                "thanh_tien": item.get("thanh_tien")
            }
            
            producer.send('chi_tiet_hoa_don_nhap_kho', event_data)
            producer.flush()
            print("đã gửi kafka chi tiết hoá đơn nhập kho")
        if tra_truoc > tong_tien:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_PREPAID_GREATER_TOTAL_MONEY), 400)
        
        if total_money != tong_tien:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_TOTAL_MONEY_NOT_SAME), 400)

        con_lai = float(total_money) - float(tra_truoc)

        # ({"tong_tien": total_money, "tra_truoc": tra_truoc, "con_lai": con_lai})

        new_hoa_don.tong_tien = total_money
        new_hoa_don.tra_truoc = tra_truoc
        new_hoa_don.con_lai   = con_lai

        db.session.commit()
        event_data = {
            "hoa_don_id": new_hoa_don.id,
            "ma_hoa_don": new_hoa_don.ma_hoa_don,
            "nha_phan_phoi_id": nha_phan_phoi_id,
            "kho_id": kho_id,
            "ngay_nhap": ngay_nhap,
            "tong_tien": total_money,
            "tra_truoc": tra_truoc,
            "con_lai": con_lai,
            "ds_san_pham_nhap": ds_san_pham_nhap
        }
        
        producer.send('hoa_don_nhap_kho', event_data)
        print("đã gửi kafka hoá đơn nhập kho")
        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        # db.session.rollback() 
        print("Lỗi:", e)
        return make_response(str(e), 500)
    
    finally:
        db.session.close()

def add_ct_hoa_don_nhap(upc, ngay_nhap, counter, hoa_don_id, san_pham_id, ctsp_id, so_luong, don_vi_tinh, ke, gia_nhap, gia_ban, chiet_khau, thanh_tien, la_qua_tang):    
    if not isExistId(id=san_pham_id, model=SanPham):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND), 400)
    if not isExistId(id=ctsp_id, model=ChiTietSanPham):
        return make_response(get_error_response(ERROR_CODES.CTSP_NOT_FOUND), 400)


    for field_name, value in [("gia_nhap", gia_nhap), ("gia_nhap", gia_nhap), ("gia_ban", gia_ban), ("chiet_khau", chiet_khau), ("thanh_tien", thanh_tien)]:
        error       = validate_number(number=value)
        if error:
            return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID, 400, f"Lỗi tại {field_name}"))
        
    counter_in_date = get_counter_detail_product_in_day(ngay_nhap=ngay_nhap, ctsp_id=ctsp_id)
    sku             = create_sku(upc=upc, ct_san_pham_id=ctsp_id, counter_detail_product_in_date=counter_in_date,date_str=ngay_nhap)

    print(123, 'trước xoá')
    # 1 - (20/100) => 1 - 0.2
    print(gia_nhap, so_luong, chiet_khau)
    thanh_tien_caculate      = gia_nhap * so_luong * (1 - chiet_khau/100)
    print('sau tính thành tiền')
    if thanh_tien != thanh_tien_caculate:
        return make_response(get_error_response(error_code=ERROR_CODES.TOTAL_AMOUNT_INVALID), 400)

    ct_nhap_kho     = ChiTietNhapKho(hoa_don_id=hoa_don_id, san_pham_id=san_pham_id, ctsp_id=ctsp_id, sku=sku, so_luong=so_luong, don_vi_tinh=don_vi_tinh, ke=ke, gia_nhap=gia_nhap, gia_ban=gia_ban, chiet_khau=chiet_khau, thanh_tien=thanh_tien, la_qua_tang=la_qua_tang)


    db.session.add(ct_nhap_kho)

    ctsp            = ChiTietSanPham.query.get(ctsp_id)

    ctsp.so_luong   = (int(ctsp.so_luong) if ctsp.so_luong else 0) + int(so_luong)
    
    ton_kho         = TonKho.query.filter_by(sku=sku).first()
    
    if ton_kho:
        ton_kho.so_luong_ton = int(ton_kho.so_luong_ton) + int(so_luong)
    else:
        new_ton_kho = TonKho(san_pham_id=san_pham_id, ctsp_id=ctsp_id, sku=sku, so_luong_ton = so_luong) 
        db.session.add(new_ton_kho)

    db.session.add(ctsp)

    return thanh_tien

def put_hoa_don_nhap_kho(hoa_don_id, kho_id, ngay_nhap, tra_truoc, ghi_chu, khoa_don):
    try:
        hoa_don = HoaDonNhapKho.query.get(hoa_don_id)
        if not hoa_don:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_NOT_FOUND), 400)
        if hoa_don.khoa_don is True:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_IS_LOCK), 400)
        if not isExistId(kho_id, Kho):
            return make_response(get_error_response(ERROR_CODES.KHO_NOT_FOUND), 400)
        
        ngay_nhap = convert_datetime(ngay_nhap)
        if ngay_nhap is False:
            return make_response(get_error_response(ERROR_CODES.DATETIME_INVALID), 500)
        
        error = validate_number(number=tra_truoc)
        if error:
            return make_response(get_error_response(ERROR_CODES.NUMBER_INVALID), 400)
        
        hoa_don.kho_id      = kho_id
        hoa_don.ngay_nhap   = ngay_nhap
        hoa_don.tra_truoc   = tra_truoc
        hoa_don.ghi_chu     = ghi_chu
        hoa_don.khoa_don    = khoa_don

        hoa_don.con_lai     = hoa_don.tong_tien - hoa_don.tra_truoc
        db.session.commit()
        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(get_error_response(ERROR_CODES.SERVER_EROR), 400)

def patch_lock(hoa_don_id, khoa_don):
    try:
        hoa_don = HoaDonNhapKho.query.get(hoa_don_id)
        
        if not hoa_don: 
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_NOT_FOUND))
            
        if khoa_don not in ["lock", "open"]:
            return make_response(get_error_response(ERROR_CODES.LOCK_STATUS_INVALID))
        print('lock or open:', khoa_don)
        
        khoa_don = True if khoa_don == 'lock' else False
        hoa_don.khoa_don = khoa_don
        print('khoa_don', khoa_don)
        db.session.commit()
        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(get_error_response(ERROR_CODES.SERVER_EROR), 400)

def get_last_record_number_bill(model):
    #model: HoaDonNhapKho or HoaDonXuatKho
    curr_year   = datetime.now().year

    #SELECT so_hoa_don FROM hoa_don_nhap_kho WHERE BETWEEN {curr_year}-01-01 AND {curr_year}-12-31 ORDER BY so_hoa_don DESC
    last_record = (
        model.query
        .filter(model.created_at.between(f"{curr_year}-01-01", f"{curr_year}-12-31"))
        .order_by(model.so_hoa_don.desc())
        .with_for_update()  # Khóa hàng để tránh race condition
        .first()
    )
    print(last_record)
    if last_record:
        return int(last_record.so_hoa_don)
    else:
        return 1

def get_counter_detail_product_in_day(ngay_nhap, ctsp_id):
    print('ngay_nhap:', ngay_nhap)
    # ngay_nhap_obj = datetime.strptime(ngay_nhap, FORMAT_DATE.MYSQL_DATE_ONLY)

    #SELECT count(*) FROM hoa_don_nhap_kho WHERE DATE(created_at) = {curr_day}
    query = text(f"""
                SELECT count(*) 
                FROM hoa_don_nhap_kho 
                LEFT JOIN 
                    chi_tiet_hoa_don_nhap_kho ON chi_tiet_hoa_don_nhap_kho.hoa_don_id = hoa_don_nhap_kho.id
                WHERE DATE(ngay_nhap) = :ngay_nhap
                    AND chi_tiet_hoa_don_nhap_kho.ctsp_id = :ctsp_id
                """)    
    count = db.session.execute(query, {"ngay_nhap": ngay_nhap, "ctsp_id": ctsp_id}).scalar()
    return count

def create_bill_code(number_bill:int, type:str):
    bill_code = f"{type}-{number_bill:06}"
    return bill_code

def tra_no_phan_phoi(hoa_don_id, tien_tra):
    hoa_don = HoaDonNhapKho.query.get(hoa_don_id)

    if not hoa_don:
        return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_NOT_FOUND), 400)
    
    con_lai = hoa_don.con_lai
    error = validate_number(number=tien_tra, start=0, end = con_lai)
    if not error:
        return error
    
    hoa_don.con_lai = con_lai - tien_tra
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def tra_hang_nhap_kho(hoa_don_id, ds_san_pham_tra):
    try:
        hoa_don = HoaDonNhapKho.query.get(hoa_don_id)

        if not hoa_don:
            return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_NOT_FOUND), 400)
        
        for row in ds_san_pham_tra:
            id = row.get("cthd_nhap_kho_id")
            so_luong_tra = row.get("so_luong_tra")
            sku = row.get("sku")

            ct_hoa_don_nhap = ChiTietNhapKho.query.get(id)
            if not ct_hoa_don_nhap:
                return make_response(get_error_response(ERROR_CODES.CTHD_NHAP_NOT_FOUND), 400)
            
            if validate_number(so_luong_tra, 0):
                return make_response(get_error_response(ERROR_CODES.SO_LUONG_TRA_GREATED_THAN_ZERO), 400)
            print(so_luong_tra)
            if so_luong_tra > ct_hoa_don_nhap.so_luong:
                return make_response(get_error_response(ERROR_CODES.HOA_DON_NHAP_SL_TRA_GREATED_THAN_SO_LUONG_SALE), 400)

            ton_kho = TonKho.query.filter_by(sku = sku, deleted_at = None).first()

            if not ton_kho:
                return make_response(get_error_response(ERROR_CODES.KHO_NOT_EXISTED_SKU), 400)
            
            if so_luong_tra > ton_kho.so_luong_ton:
                return make_response(get_error_response(ERROR_CODES.KHO_NOT_QUANTITY_FOR_RETURNS), 400)
            
            ct_hoa_don_nhap.so_luong = int(ct_hoa_don_nhap.so_luong) - int(so_luong_tra)

            if ct_hoa_don_nhap.so_luong == 0:
                ct_hoa_don_nhap.soft_delete()
            
            ton_kho.so_luong_ton -= so_luong_tra

        db.session.commit()
        return get_error_response(ERROR_CODES.SUCCESS)
    except Exception as e:
        print(e)
        return make_response(str(e), 500)
    finally:
        db.session.close()