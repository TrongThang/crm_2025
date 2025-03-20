from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.services.dbService import excute_select_data
from crm_app.models.NhanVien import NhanVien
from crm_app.models.ChucVu import ChucVu
from crm_app.models.HoaDonXuatKho import HoaDonXuatKho
from sqlalchemy import or_
from crm_app import db
from crm_app.helpers.redis import get_permission_by_role

def get_nhan_vien_by_username(username, chuc_vu_id):
    filter = '[{"field": "ten_dang_nhap", "condition": "=", "value": "' + username + '"}]'
    get_attr = "ten_dang_nhap,ho_ten, email, dien_thoai, dia_chi, chuc_vu.ten as chuc_vu, chuc_vu.id as chuc_vu_id"
    get_table = "nhan_vien"

    query_join = text(""" LEFT JOIN chuc_vu ON chuc_vu.id = nhan_vien.chuc_vu_id """)

    data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, query_join=query_join)
    response_data = data.get("data")
    print(data)
    ds_quyen = [q.decode('utf-8') for q in get_permission_by_role(chuc_vu_id=chuc_vu_id)]
    
    response_data[0]["ds_quyen"] = ds_quyen
    response_data = {"data":response_data}
    return get_error_response(ERROR_CODES.SUCCESS, result=data)

def get_nhan_vien(filter, limit, page, sort, order):
    get_table = 'nhan_vien'
    get_attr = ' ten_dang_nhap,ho_ten, email, dien_thoai, dia_chi, avatar, chuc_vu.ten as chuc_vu, chuc_vu.id as chuc_vu_id, '
    query_join = text(""" LEFT JOIN chuc_vu ON chuc_vu.id = nhan_vien.chuc_vu_id """)
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)
    print('response_data:', response_data)
    return get_error_response(ERROR_CODES.SUCCESS, result=response_data)

def post_nhan_vien(username, ho_ten, email, dien_thoai, dia_chi, avatar, chuc_vu_id):
    print(username)
    error = validate_name(username, model=NhanVien)
    if error:
        return error
    
    isExisted = isExistId(id=chuc_vu_id, model=ChucVu)
    if isExisted != True:
        return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 401)
    
    if username is not None:
        nhan_vien = NhanVien.query.filter_by(ten_dang_nhap=username).first()
        print(nhan_vien)
        if nhan_vien:
            return make_response(get_error_response(ERROR_CODES.USERNAME_EXISTED), 401)

    error = validate_name(ho_ten, model=NhanVien, is_unique=False)
    if error:
        return error
    
    error = validate_email(email)
    if error:
        return error

    error = validate_phone(dien_thoai)
    if error:
        return error
    
    if isExistId(id=chuc_vu_id, model=ChucVu) is False:
        return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 401)

    nhan_vien = NhanVien(ho_ten=ho_ten, ten_dang_nhap=username, mat_khau='1', email=email, dia_chi=dia_chi, dien_thoai=dien_thoai, avatar=avatar, chuc_vu_id=chuc_vu_id)
    db.session.add(nhan_vien)
    db.session.commit()
    return make_response(get_error_response(ERROR_CODES.SUCCESS),200)


def put_nhan_vien(id, ho_ten, username, email, dien_thoai, dia_chi, avatar, chuc_vu_id):
    nhan_vien = NhanVien.query.get(id)
    print(id)
    print(nhan_vien)
    if nhan_vien is None:
        return make_response(get_error_response(ERROR_CODES.NHAN_VIEN_NOT_FOUND), 401)

    if chuc_vu_id is not None:
        isExisted = isExistId(id=chuc_vu_id, model=ChucVu)
        if isExisted != True:
            return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 401)
        nhan_vien.chuc_vu_id = chuc_vu_id
    
    if username is not None:
        if username != nhan_vien.ten_dang_nhap:
            check_username = NhanVien.query.filter_by(ten_dang_nhap=username).first()
            if check_username:
                return make_response(ERROR_CODES.USERNAME_EXISTED)
            nhan_vien.ten_dang_nhap = username

    if ho_ten is not None:
        if len(ho_ten) > 255 or len(ho_ten) <= 0:
            return get_error_response(ERROR_CODES.NHAN_VIEN_NAME_LENGTH) 
        nhan_vien.ho_ten = ho_ten
    if email is not None:
        error = validate_email(email=email)
        if error:
            return error
        
    if dien_thoai is not None:
        error = validate_phone(phone=dien_thoai)
        if error:
            return error

    if dia_chi is not None:
        nhan_vien.chuc_vu = dia_chi

    if avatar is not None:
        print('cập nhật avatar')
        nhan_vien.avatar = avatar
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)


def delete_nhan_vien(id):
    nhan_vien = NhanVien.query.get(id)
    if nhan_vien is None:
        return get_error_response(ERROR_CODES.NHAN_VIEN_NOT_FOUND)
    
    if HoaDonXuatKho.query.filter(or_(nhan_vien_giao_hang_id=id, nhan_vien_sale_id = id), deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.NHAN_VIEN_REFERENCE_HOA_DON_XUAT), 401)
    
    nhan_vien.soft_delete()
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)