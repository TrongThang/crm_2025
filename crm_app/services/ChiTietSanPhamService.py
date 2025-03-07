from crm_app.models.ChiTietSanPham import ChiTietSanPham
from crm_app.models.SanPham import SanPham
from crm_app.services.utils import *
from crm_app.services.dbService import excute_select_data
from crm_app import db


from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietXuatKho import ChiTietXuatKho
from crm_app.models.TonKho import TonKho


def get_chi_tiet_san_pham_by_san_pham(san_pham_id):
    filter = '[{"field": "id", "condition": "=", "value": ' + str(san_pham_id) + '}]'

    get_attr = "san_pham_id, ten_phan_loai, hinh_anh, trang_thai, khong_phan_loai"
    get_table = "chi_tiet_san_pham"

    filter = '[{"field": "san_pham_id", "condition": "=", "value": ' + str(san_pham_id) + '}, {"field": "khong_phan_loai", "condition": "=", "value": 0}]'
    lst_ctsp = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter)

    return get_error_response(ERROR_CODES.SUCCESS, result=lst_ctsp)

def add_chi_tiet_san_pham(san_pham_id, ten_phan_loai, file_phan_loai=None, trang_thai_pl=None):
    print(f"san_pham_id: {san_pham_id}, ten_phan_loai: {ten_phan_loai}, file_phan_loai: {file_phan_loai}, trang_thai_pl: {trang_thai_pl}")
    
    # trang_thai_pl = get_status_by_object(trang_thai_pl)
    # if not trang_thai_pl:
    #     return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND_TRANG_THAI), 401)
    
    khong_phan_loai = True
    
    if ten_phan_loai is not None:
        error = validate_name(name=ten_phan_loai, model=ChiTietSanPham)
        if error:
            return error
        khong_phan_loai = False

    trang_thai_pl = True if trang_thai_pl == '1' else False
    print('trước thêm chi tiết sản phẩm')
    chi_tiet = ChiTietSanPham(san_pham_id=san_pham_id, ten_phan_loai=ten_phan_loai, hinh_anh=file_phan_loai, trang_thai=trang_thai_pl, khong_phan_loai=khong_phan_loai)
    print('sau thêm chi tiết sản phẩm')

    db.session.add(chi_tiet)

    return get_error_response(ERROR_CODES.SUCCESS)

def update_chi_tiet_san_pham(id, ten_phan_loai, file_phan_loai, trang_thai):
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
        
    if trang_thai is not None:
        chi_tiet.trang_thai = trang_thai
    
    if file_phan_loai is not None:
        chi_tiet.hinh_anh = file_phan_loai

    db.session.commit()    

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_one_chi_tiet_san_pham (id = None):
    chi_tiet = ChiTietSanPham.query.get(id)

    if chi_tiet is None:
        return make_response(get_error_response(ERROR_CODES.CTSP_INVALID_ID), 401)
    
    result = check_detail_product_reference(ctsp_id=ct.id)

    if result is True:
        chi_tiet.soft_delete()
        db.session.commit()
    else:
        return result

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_many_chi_tiet_san_pham (san_pham_id = None):
    if san_pham_id is not None:
        list_chi_tiet = ChiTietSanPham.query.filter_by(san_pham_id=san_pham_id)
        for ct in list_chi_tiet:
            chi_tiet = ChiTietSanPham.query.get(ct.id)

            if chi_tiet:
                result = check_detail_product_reference(ctsp_id=ct.id)

                if result is True:
                    chi_tiet.soft_delete()
                else:
                    return result
        db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def check_detail_product_reference(ctsp_id):
    if TonKho.query.filter_by(ctsp_id=ctsp_id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.CTSP_REFERENCE_TON_KHO),401)
    
    if ChiTietNhapKho.query.filter_by(ctsp_id=ctsp_id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.CTSP_REFERENCE_CHI_TIET_NHAP_HD),401)
    
    if ChiTietXuatKho.query.filter_by(ctsp_id=ctsp_id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.CTSP_REFERENCE_CHI_TIET_XUAT_HD), 401)
    
    return True