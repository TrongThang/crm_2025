from flask import make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.dbService import *
from crm_app.models.BaoHanh import BaoHanh
from crm_app import db
from sqlalchemy import text
import math 

def get_bao_hanh (filter, limit, page, sort, order):
    get_table = 'thoi_gian_bao_hanh'
    get_attr = 'ten'

    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)
    
    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_bao_hanh (name):
    error = validate_name(
        name= name,
        model=BaoHanh,
    )
    if error:
        return error
    
    newThoiGianBaoHanh = BaoHanh(ten=name)
    db.session.add(newThoiGianBaoHanh)
    db.session.commit()
    db.session.flush()

    response_data = newThoiGianBaoHanh.to_dict()
    return make_response(get_error_response(error_code=ERROR_CODES.SUCCESS, result=response_data), 200)

def put_bao_hanh (id, name):
    error = validate_name(
        name = name,
        model=BaoHanh,
        existing_id=id,
        is_unique=True
    )
    if error:
        return error
    
    bao_hanh = BaoHanh.query.get(id)
    
    if bao_hanh is None:
        return make_response(get_error_response(ERROR_CODES.DVT_NOT_FOUND), 401)

    bao_hanh.ten = name

    db.session.commit()

    return make_response(get_error_response(error_code=ERROR_CODES.SUCCESS), 200)

def delete_bao_hanh(id):
    bao_hanh = BaoHanh.query.get(id)
    
    if bao_hanh is None:
        return (get_error_response(error_code=ERROR_CODES.BAO_HANH_NOT_FOUND), 401)
    bao_hanh.soft_delete()

    return make_response(get_error_response(error_code=ERROR_CODES.SUCCESS), 200)