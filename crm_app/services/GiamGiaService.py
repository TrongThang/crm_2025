from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.models.GiamGia import GiamGia
from crm_app import db
from sqlalchemy import text

def get_giam_gia (kw = None, value = None):
    kw = f"%{kw}%" if kw else "%"
    value = value if value else ""

    query = text("SELECT id, ten, gia_tri, created_at, updated_at, deleted_at FROM loai_giam_gia WHERE ten LIKE :kw AND gia_tri = :value")
    data = db.session.execute(query, {'kw': kw, 'value': value}).fetchall()

    result = [{
        'id': row.id,
        'ten': row.ten,
        'gia_tri': row.gia_tri,
        'created_at': row.created_at,
        'updated_at': row.updated_at,
        'deleted_at': row.deleted_at,
    }
    for row in data
    ]

    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=result)

def post_giam_gia (name, value):
    error = validate_name(name = name, model=GiamGia)
    if error:
        return error
    
    error = validate_number(number=value, model=GiamGia)
    if error:
        return error

    newLGiamGia = GiamGia(ten=name, gia_tri=value)
    db.session.add(newLGiamGia)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

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
    db.session.delete(giam_gia)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)