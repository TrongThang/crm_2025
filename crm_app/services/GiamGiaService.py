from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.models.GiamGia import GiamGia
from crm_app import db
from sqlalchemy import text
import math

def get_giam_gia (limit, page, filter, order, sort):
    build_where = build_where_query(filter=filter)
    limit = limit if limit else 10
    page = page if page else 1
    skip = limit * (page - 1)
    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {sort} {opt_order} " if sort else ""

    query = text(f"""
                SELECT id, ten, gia_tri, created_at, updated_at, deleted_at 
                FROM loai_giam_gia
                {build_where}
                {build_sort}
                LIMIT {limit}
                OFFSET {skip}
                """)
    data = db.session.execute(query).fetchall()
    total_page = math.ceil(len(data)/limit)

    result = [{
        'ID': row.id,
        'ten': row.ten,
        'gia_tri': row.gia_tri,
        'CreatedAt': row.created_at,
        'UpdatedAt': row.updated_at,
        'DeletedAt': row.deleted_at,
    }
    for row in data
    ]
    response_data = {"data": result, "total_page": total_page}

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