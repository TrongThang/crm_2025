from flask import make_response 
from crm_app.docs.containts import ERROR_CODES
from crm_app.services.utils import *
from crm_app.services.dbService import *
from crm_app.models.KhachHang import KhachHang 
from crm_app import db

def get_khach_hang(filter, limit, page, sort, order):
    get_table = 'khach_hang'
    get_attr = 'ho_ten, dia_chi, dien_thoai'
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)

    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_khach_hang(name, address, phone):
    error = validate_name(name=name, model=KhachHang)
    if error:
        return make_response(error, 401)
    
    error = validate_phone(phone=phone)
    if error:
        return make_response(error, 401)
    
    new_khach_hang = KhachHang(ho_ten=name, dia_chi=address, dien_thoai=phone)
    db.session.add(new_khach_hang)
    db.session.commit()

    result = new_khach_hang.to_dict()
    return get_error_response(ERROR_CODES.SUCCESS, result=result)

def put_khach_hang(id, name, address, phone):
    khach_hang = KhachHang.query.get(id)
    if khach_hang is None:
        return make_response(get_error_response(ERROR_CODES.NOT_FOUND), 401)
    
    if name is not None:
        error = validate_name(name=name, model=KhachHang, is_unique=False)
        if error:
            return make_response(error, 401)
        khach_hang.ho_ten = name
    
    if address is not None:
        error = validate_name(name=name, model=KhachHang, is_unique=False)
        if error:
            return make_response(error, 401)
        khach_hang.dia_chi = address
    
    if phone is not None:
        error = validate_phone(phone=phone)
        if error:
            return error
        khach_hang.dien_thoai = phone

    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def delete_khach_hang(id):
    khach_hang = KhachHang.query.get(id)

    if khach_hang is None:
        return make_response(get_error_response(ERROR_CODES.NOT_FOUND), 401)
    
    khach_hang.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)