from flask import jsonify, make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import build_where_query
from crm_app.models.BaoHanh import BaoHanh
from crm_app import db
from sqlalchemy import text
import math 

def get_bao_hanh (filter, limit, page, sort, order):
    build_where = build_where_query(filter=filter) if filter else ''
    limit = limit if limit else 10
    page = page if page else 1
    skip = limit * (page - 1)
    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {sort} {opt_order} " if sort else ""
    
    query = text(f"""
                SELECT id, ten, created_at, updated_at, deleted_at
                FROM thoi_gian_bao_hanh 
                {build_where}
                {build_sort}
                LIMIT {limit}
                OFFSET {skip}
                """)
    data = db.session.execute(query).fetchall()
    total_page = math.ceil(len(data)/limit)

    result = [{
        'id': row.id,
        'ten': row.ten,
        'created_at': row.created_at,
        'updated_at': row.updated_at,
        'deleted_at': row.deleted_at,
    }
    for row in data
    ]
    response_data = {"data": result, "total_page": total_page}
    return make_response(get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data), 200)

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
    db.session.flush()

    response_data = newThoiGianBaoHanh.to_dict()
    return make_response(get_error_response(error_code=ERROR_CODES.SUCCESS, result=response_data), 200)

def put_bao_hanh (id, name):
    error = validate_number(
        number = name,
        model=BaoHanh
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