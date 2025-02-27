from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app.services.utils import *
from crm_app import db

def add_chi_tiet_san_pham(san_pham_id, ten_phan_loai, file_phan_loai, gia_nhap, gia_ban, so_luong, trang_thai_pl):
    error = validate_name(name=ten_phan_loai, model=ChiTietSanPham)
    if error:
        return error
    
    error = validate_number(number=gia_ban, model=ChiTietSanPham)
    if error:
        return error
    
    error = validate_number(number=gia_nhap, model=ChiTietSanPham)
    if error:
        return error
    
    if gia_nhap > gia_ban:
        return get_error_response(ERROR_CODES.COST_PRICE_GREATER_SELL_PRICE)
    
    error = validate_number(number=so_luong, model=ChiTietSanPham)
    if error:
        return error
    
    khong_phan_loai = True
    
    if ten_phan_loai is not None:
        khong_phan_loai = False

    upload = save_uploaded_file(file_phan_loai, "chi_tiet_sp", prefix=f'chi_tiet_sp_{ten_phan_loai}_')
    if upload['errorCode'] == ERROR_CODES.SUCCESS:
        filename = upload['filename']
    elif (upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND):
        filename = None
    else:
        return get_error_response(upload['errorCode'])

    chi_tiet = ChiTietSanPham(san_pham_id=san_pham_id, ten_phan_loai=ten_phan_loai, hinh_anh=filename, gia_nhap=gia_nhap, gia_ban=gia_ban, so_luong=so_luong, trang_thai=trang_thai_pl, khong_phan_loai=khong_phan_loai)

    db.session.add(chi_tiet)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def update_chi_tiet_san_pham(id, san_pham_id, ten_phan_loai, file_phan_loai, gia_nhap, gia_ban, so_luong, trang_thai_pl):
    chi_tiet = ChiTietSanPham.query.get(id)
    if chi_tiet is None:
        return get_error_response(ERROR_CODES.CTSP_NOT_FOUND)
    
    if ten_phan_loai is not None:
        error = validate_name(name=ten_phan_loai, model=ChiTietSanPham)
        if error:
            return error
        chi_tiet.ten_phan_loai = ten_phan_loai
        chi_tiet.khong_phan_loai = False
    else:
        chi_tiet.khong_phan_loai = True
    if so_luong is not None:
        error = validate_number(number=so_luong, model=ChiTietSanPham)
        if error:
            return error
        chi_tiet.so_luong = so_luong

    if gia_nhap is not None:
        error = validate_number(number=gia_nhap, model=ChiTietSanPham)
        if error:
            return error
        if gia_ban is not None:
            error = validate_number(number=gia_ban, model=ChiTietSanPham)
            if error:
                return error
            
            if gia_nhap > gia_ban:
                return get_error_response(ERROR_CODES.COST_PRICE_GREATER_SELL_PRICE)
        else:
            if gia_nhap > chi_tiet.gia_ban:
                return get_error_response(ERROR_CODES.COST_PRICE_GREATER_SELL_PRICE)
            chi_tiet.gia_ban = gia_ban

        chi_tiet.gia_nhap = gia_nhap
        
    if trang_thai_pl is not None:
        chi_tiet.trang_thai = trang_thai_pl
    
    if file_phan_loai is not None:
        upload = save_uploaded_file(file_phan_loai, "chi_tiet_sp", filename=chi_tiet.hinh_anh, prefix=f'chi_tiet_sp_{ten_phan_loai}_')
        if upload['errorCode'] == ERROR_CODES.SUCCESS:
            filename = upload['filename']
        elif (upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND):
            filename = None
        else:
            return get_error_response(upload['errorCode'])

    db.session.commit()    

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_one_chi_tiet_san_pham (id = None):
    chi_tiet = ChiTietSanPham.query.get(id)

    if chi_tiet is None:
        return get_error_response(ERROR_CODES.CTSP_INVALID_ID)
    
    chi_tiet.soft_delete()
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_many_chi_tiet_san_pham (san_pham_id = None):
    if san_pham_id is not None:
        list_chi_tiet = ChiTietSanPham.query.filter_by(san_pham_id=san_pham_id)
        for ct in list_chi_tiet:
            chi_tiet = ChiTietSanPham.query.get(ct.id)
            chi_tiet.soft_delete()
        db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)