from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.models.DonViTinh import DonViTinh
from crm_app import db
from sqlalchemy import text
import math

def get_don_vi_tinh (filter, limit, page, order, sort):
    build_where = build_where_query(filter=filter) if filter else ''
    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {sort} {opt_order} " if sort else ""
    limit = limit if limit else 10
    page = page if page else 1
    skip = limit * (page - 1)

    query = text(f"""
                SELECT 
                    id, ten, created_at, updated_at, deleted_at 
                FROM don_vi_tinh 
                {build_where} 
                {build_sort} 
                LIMIT {limit}
                OFFSET {skip}
                """)
    data = db.session.execute(query).fetchall()

    result = [{
        'ID': dvt.id,
        'ten': dvt.ten,
        'CreatedAt': dvt.created_at,
        'UpdatedAt': dvt.updated_at,
        'DeletedAt': dvt.deleted_at,
    }
    for dvt in data
    ]
    total_page = math.ceil(len(data)/limit)
    response_data = {"data": result, "total_page": total_page}
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

    don_vi_tinh.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)