from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.models.BaoHanh import BaoHanh
from crm_app import db
from sqlalchemy import text

def get_bao_hanh (kw = None):
    kw = f"%{kw}%" if kw else "%"
    query = text("SELECT id, ten, created_at, updated_at, deleted_at FROM thoi_gian_bao_hanh WHERE ten LIKE :kw")
    data = db.session.execute(query, {'kw': kw}).fetchall()

    result = [{
        'id': row.id,
        'ten': row.ten,
        'created_at': row.created_at,
        'updated_at': row.updated_at,
        'deleted_at': row.deleted_at,
    }
    for row in data
    ]

    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=result)

def post_bao_hanh (name):
    error = validate_number(
        number= name,
        model=BaoHanh,
    )
    if error:
        return error
    
    newThoiGianBaoHanh = BaoHanh(ten=name)
    db.session.add(newThoiGianBaoHanh)
    db.session.commit()

    return jsonify({"errorCode": ERROR_CODES.SUCCESS.value, "message": MESSAGES.SUCCESS.value})

def put_bao_hanh (id, name):
    error = validate_number(
        number = name,
        model=BaoHanh
    )
    if error:
        return error
    
    bao_hanh = BaoHanh.query.get(id)
    
    if bao_hanh is None:
        return get_error_response(ERROR_CODES.DVT_NOT_FOUND)

    bao_hanh.ten = name

    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_bao_hanh(id):
    bao_hanh = BaoHanh.query.get(id)

    db.session.delete(bao_hanh)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)