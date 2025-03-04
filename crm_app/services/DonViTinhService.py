from flask import jsonify, make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.dbService import *
from crm_app.models.DonViTinh import DonViTinh
from crm_app import db
from sqlalchemy import text
import math

def get_don_vi_tinh (filter, limit, page, order, sort):
    get_table = 'don_vi_tinh'
    get_attr = 'ten'

    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)
    
    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_don_vi_tinh (ten):
    error = validate_name(
        name = ten,
        model=DonViTinh,
    )
    if error:
        return error
    
    newDVT = DonViTinh(ten=ten)
    db.session.add(newDVT)
    db.session.commit()

    result = newDVT.to_dict()
    
    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=result)

def put_don_vi_tinh (id, name):
    print("name:", name)
    error = validate_name(
        name = name,
        model=DonViTinh,
        is_unique=True,
        existing_id=id
    )
    if error:
        return error
    
    don_vi_tinh = DonViTinh.query.get(id)
    
    if don_vi_tinh is None:
        return make_response(get_error_response(ERROR_CODES.DVT_NOT_FOUND), 401)

    don_vi_tinh.ten = name

    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_don_vi_tinh(id):
    don_vi_tinh = DonViTinh.query.get(id)

    don_vi_tinh.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)