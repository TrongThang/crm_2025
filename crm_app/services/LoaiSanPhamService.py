from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.models.LoaiSanPham import LoaiSanPham
from crm_app import db
from sqlalchemy import text
import math

def get_loai_sp (filter, limit, page, sort, order):
    print(filter)
    build_where = build_where_query(filter=filter) if filter else ''
    limit = limit
    page = page
    skip = int(limit) * (int(page) - 1) if limit and page else 0
    
    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {sort} {opt_order} " if sort else ""
    build_limit = f" LIMIT {limit}" if limit else ""
    build_offset = f" OFFSET {skip}" if limit and page else ""

    build_where = f"{build_where} AND deleted_at IS NULL" if build_where else ' WHERE deleted_at IS NULL'
    query_all = text(f"""
                SELECT id, ten, hinh_anh, created_at, updated_at, deleted_at 
                FROM loai_san_pham
                {build_where}
                """)
    query = text(f"""
                {query_all}
                {build_sort}
                {build_limit}
                {build_offset}
            """)
    print("query:", query)
    print("query_all:", query_all)
    data = db.session.execute(query).fetchall()
    limit = int(limit) if limit else 1
    all_item = len(db.session.execute(query_all).fetchall())
    total_page = math.ceil(all_item/limit)
    print("total_page:", all_item, '/',  limit)
    result = [{
        'ID': row.id,
        'ten': row.ten,
        'hinh_anh': row.hinh_anh,
        'CreatedAt': row.created_at,
        'UpdatedAt': row.updated_at,
        'DeletedAt': row.deleted_at,
    }
    for row in data
    ]
    
    response_data = {"data": result, "total_page": total_page}
    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_loai_sp (name, file):
    error = validate_name(name=name, model=LoaiSanPham)
    if error:
        return error
    
    upload = save_uploaded_file(file, 'loai_sp',prefix='loai_sp_')  
    if(upload['errorCode'] == ERROR_CODES.SUCCESS):
        filename = upload['filename'] 
    elif (upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND):
        filename = None
    else:
        return get_error_response(upload['errorCode'])
    
    loai_sp = LoaiSanPham(ten=name, hinh_anh=filename)
    db.session.add(loai_sp)
    db.session.commit()

    result = loai_sp.to_dict()
    return get_error_response(ERROR_CODES.SUCCESS, result=result)

def put_loai_sp (id, name, file):
    loai_sp = LoaiSanPham.query.get(id)
    if loai_sp is None:
        return get_error_response(ERROR_CODES.LOAI_SP_NOT_FOUND)
    if name is not None:
        error = validate_name(name=name, model=LoaiSanPham, is_unique=False)
        if error:
            return error
        loai_sp.ten = name
    print("file:", file)
    if file is not None:
        print("chỉnh sửa hình")
        upload = save_uploaded_file(file, "loai_sp", filename=loai_sp.hinh_anh, prefix='loai_sp')
        if(upload['errorCode'] == ERROR_CODES.SUCCESS):
            loai_sp.hinh_anh = upload['filename']
        elif upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND:
            pass
        else:
            return get_error_response(upload['errorCode'])
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def delete_loai_sp (id):
    loai_sp = LoaiSanPham.query.get(id)

    if loai_sp is None:
        return get_error_response(ERROR_CODES.LOAI_SP_NOT_FOUND)
    if loai_sp.hinh_anh:
        result = delete_file('loai_sp', loai_sp.hinh_anh)
    # if result['errorCode'] == ERROR_CODES.SUCCESS:
    loai_sp.soft_delete()
    return get_error_response(ERROR_CODES.SUCCESS)
    