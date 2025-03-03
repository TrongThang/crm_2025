from flask import jsonify, make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.services.dbService import *
from crm_app.models.GiamGia import GiamGia
from crm_app import db
from sqlalchemy import text
import math

def get_giam_gia (limit, page, filter, order, sort):
    get_table = 'don_vi_tinh'
    get_attr = 'ten, gia_tri'
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)

    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_giam_gia (ten, value):
    error = validate_name(ten = ten, model=GiamGia)
    if error:
        return error
    
    error = validate_number(number=value, model=GiamGia)
    if error:
        return error

    newLGiamGia = GiamGia(ten=ten, gia_tri=value)
    db.session.add(newLGiamGia)
    db.session.commit()

    result = newLGiamGia.to_dict()
    return get_error_response(ERROR_CODES.SUCCESS, result=result)

def put_giam_gia (id, name, value):
    giam_gia = GiamGia.query.get(id)
    
    if giam_gia is None:
        return get_error_response(ERROR_CODES.GIAM_GIA_NOT_FOUND)

    if name is not None:
        error = validate_name(
                    name = name,
                    model=GiamGia,
                    existing_id=id
                )
        if error:
            return error
        giam_gia.ten = name

    if value is not None:
        error = validate_number(number=value, model=GiamGia)
        if error:
            return error
        
        if value > 90:
            return get_error_response(ERROR_CODES.GIAM_GIA_INVALID_PERCENT)
        
        giam_gia.gia_tri = value
    

    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_giam_gia(id):
    giam_gia = GiamGia.query.get(id)

    if giam_gia is None:
        return get_error_response(ERROR_CODES.GIAM_GIA_NOT_FOUND)
    giam_gia.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)