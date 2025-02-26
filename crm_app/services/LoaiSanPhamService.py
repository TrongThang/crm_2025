from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.models.LoaiSanPham import LoaiSanPham
from crm_app import db
from sqlalchemy import text

def get_loai_sp (filter):
    build_where = build_where_query(filter=filter)

    query = text(f"SELECT id, ten, hinh_anh, created_at, updated_at, deleted_at FROM loai_san_pham {build_where}")
    data = db.session.execute(query).fetchall()

    result = [{
        'id': row.id,
        'ten': row.ten,
        'hinh_anh': row.hinh_anh,
        'created_at': row.created_at,
        'updated_at': row.updated_at,
        'deleted_at': row.deleted_at,
    }
    for row in data
    ]

    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=result)

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
    return get_error_response(ERROR_CODES.SUCCESS)

def put_loai_sp (id, name, file):
    loai_sp = LoaiSanPham.query.get(id)
    if loai_sp is None:
        return get_error_response(ERROR_CODES.LOAI_SP_NOT_FOUND)
    if name is not None:
        error = validate_name(name=name, model=LoaiSanPham)
        if error:
            return error
        loai_sp.ten = name
    if file is not None:
        upload = save_uploaded_file(file, "loai_sp", filename=loai_sp.hinh_anh,prefix='loai_sp')
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
    db.session.delete(loai_sp)
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)
    