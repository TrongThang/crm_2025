from flask import make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.services.dbService import *
from crm_app.models.LoaiSanPham import LoaiSanPham
from crm_app import db
from sqlalchemy import text
import math

def get_loai_sp (filter, limit, page, sort, order):
    get_table = 'loai_san_pham'
    get_attr = 'ten, hinh_anh'

    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)
    
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
        error = validate_name(name=name, model=LoaiSanPham, is_unique=False, existing_id=id)
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
        return make_response(get_error_response(ERROR_CODES.LOAI_SP_NOT_FOUND), 401)
    if loai_sp.hinh_anh:
        result = delete_file('loai_sp', loai_sp.hinh_anh)
    # if result['errorCode'] == ERROR_CODES.SUCCESS:
    loai_sp.soft_delete()
    return get_error_response(ERROR_CODES.SUCCESS)
    