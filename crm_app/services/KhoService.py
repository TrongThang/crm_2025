from flask import make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.services.dbService import *
from crm_app.models.Kho import Kho
from crm_app.models.HoaDonNhapKho import HoaDonNhapKho
from crm_app.models.HoaDonXuatKho import HoaDonXuatKho
from crm_app import db
from sqlalchemy import text
import math

def get_ton_kho(ctsp_id):
    filter = '[{"field": "chi_tiet_hoa_don_nhap_kho.ctsp_id", "condition": "=", "value":' + str(ctsp_id) + '}]'
    get_table = 'ton_kho'
    get_attr = """
        ton_kho.ctsp_id AS ctsp_id, ton_kho.san_pham_id AS san_pham_id, san_pham.ten AS san_pham, upc, so_luong_ton,  chi_tiet_san_pham.ten_phan_loai AS ctsp_ten,ton_kho.sku, chi_tiet_hoa_don_nhap_kho.gia_ban, chi_tiet_hoa_don_nhap_kho.han_su_dung, chi_tiet_hoa_don_nhap_kho.don_vi_tinh
    """
    query_join = """
        LEFT JOIN san_pham ON san_pham.id = ton_kho.san_pham_id
        LEFT JOIN chi_tiet_san_pham ON chi_tiet_san_pham.id = ton_kho.ctsp_id
        LEFT JOIN chi_tiet_hoa_don_nhap_kho ON chi_tiet_hoa_don_nhap_kho.ctsp_id = chi_tiet_san_pham.id
    """
    
    data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, query_join=query_join)

    return get_error_response(ERROR_CODES.SUCCESS, result=data)

def get_kho (filter, limit, page, sort, order):
    get_table = 'kho'
    get_attr = 'ten, dia_chi'
    print(filter)
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)
    print('response_data:',response_data)
    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_kho (name, address):
    error = validate_name(name=name, model=Kho)
    if error:
        return error
    
    new_kho = Kho(ten=name, dia_chi=address)
    db.session.add(new_kho)
    db.session.commit()

    result = new_kho.to_dict()
    return get_error_response(ERROR_CODES.SUCCESS, result=result)

def put_kho (id, name, address):
    kho = Kho.query.get(id)
    if kho is None:
        return get_error_response(ERROR_CODES.KHO_NOT_FOUND)
    if name is not None:
        error = validate_name(name=name, model=Kho, is_unique=True, existing_id=id)
        if error:
            return error
        kho.ten = name
    if address is not None:
        kho.dia_chi = address
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def delete_kho (id):
    kho = Kho.query.get(id)

    if kho is None:
        return make_response(get_error_response(ERROR_CODES.KHO_NOT_FOUND), 401)
    
    if HoaDonNhapKho.query.filter_by(kho_id=id, deleted_at=None).first():
        return make_response(get_error_response(ERROR_CODES.KHO_REFERENCE_HOA_DON_NHAP), 401)
    
    kho.soft_delete()
    return get_error_response(ERROR_CODES.SUCCESS)