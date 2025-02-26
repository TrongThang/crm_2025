from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.models.DonViTinh import DonViTinh
from crm_app import db
from sqlalchemy import text

def get_don_vi_tinh (filter = None):
    build_where = build_where_query(filter=filter) if filter else ''
    query = text(f"""SELECT id, ten, created_at, updated_at, deleted_at FROM don_vi_tinh {build_where}""")
    data = db.session.execute(query).fetchall()

    result = [{
        'id': dvt.id,
        'ten': dvt.ten,
        'created_at': dvt.created_at,
        'updated_at': dvt.updated_at,
        'deleted_at': dvt.deleted_at,
    }
    for dvt in data
    ]

    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=result)

def post_don_vi_tinh (name):
    error = validate_name(
        name = name,
        model=DonViTinh,
    )
    if error:
        return error
    
    newDVT = DonViTinh(ten=name)
    db.session.add(newDVT)
    db.session.commit()

    return jsonify({"errorCode": ERROR_CODES.SUCCESS.value, "message": MESSAGES.SUCCESS.value})

def put_don_vi_tinh (id, name):
    error = validate_name(
        name = name,
        model=DonViTinh,
        existing_id=id
    )
    if error:
        return error
    
    don_vi_tinh = DonViTinh.query.get(id)
    
    if don_vi_tinh is None:
        return get_error_response(ERROR_CODES.DVT_NOT_FOUND)

    don_vi_tinh.ten = name

    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_don_vi_tinh(id):
    don_vi_tinh = DonViTinh.query.get(id)

    db.session.delete(don_vi_tinh)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)