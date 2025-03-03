from flask import make_response 
from crm_app.docs.containts import ERROR_CODES
from crm_app.services.utils import *
from crm_app.services.dbService import *
from crm_app.models.NhaPhanPhoi import NhaPhanPhoi 
from crm_app.models.SanPham import SanPham 
from crm_app.models.SanPhamNhaPhanPhoi import SanPhamNhaPhanPhoi 
from crm_app import db

def get_nha_phan_phoi(filter, limit, page, sort, order):
    get_table = 'nha_phan_phoi'
    get_attr = 'ten, dia_chi, dien_thoai, email'
    
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)
    return get_error_response(error_code=ERROR_CODES.SUCCESS,result=response_data)

def post_nha_phan_phoi(name, address, phone, email, ds_san_pham = None):
    error = validate_name(name=name, model=NhaPhanPhoi)
    if error:
        return make_response(error, 401)
    
    error = validate_phone(phone=phone)
    if error:
        return make_response(error, 401)
    
    error = validate_email(email=email)
    if error:
        return error
    
    new_nha_phan_phoi = NhaPhanPhoi(ten=name, dia_chi=address, dien_thoai=phone, email=email)
    db.session.add(new_nha_phan_phoi)
    
    if ds_san_pham:
        db.session.flush()
        for san_pham in ds_san_pham:
            san_pham_id = san_pham.get("id")
            if san_pham_id:
                if isExistId(id=san_pham_id, model=SanPham):
                    print('add product with npp')
                    san_pham_nha_phan_phoi = SanPhamNhaPhanPhoi(nha_phan_phoi_id=new_nha_phan_phoi.id, san_pham_id=san_pham_id)
                    db.session.add(san_pham_nha_phan_phoi)

    db.session.commit()

    result = new_nha_phan_phoi.to_dict()
    return get_error_response(ERROR_CODES.SUCCESS, result=result)

def put_nha_phan_phoi(id, name, address, phone, email, ds_san_pham):
    nha_phan_phoi = NhaPhanPhoi.query.get(id)
    if nha_phan_phoi is None:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)
    
    if name is not None:
        error = validate_name(name=name, model=NhaPhanPhoi, is_unique=False)
        if error:
            return make_response(error, 401)
        nha_phan_phoi.ten = name
    
    if address is not None:
        print("address:", address)
        error = validate_name(name=name, model=NhaPhanPhoi, is_unique=False)
        if error:
            return make_response(error, 401)
        nha_phan_phoi.dia_chi = address
    
    if phone is not None:
        error = validate_phone(phone=phone)
        if error:
            return error
        nha_phan_phoi.dien_thoai = phone
        
    if email is not None:
        error = validate_email(email=email)
        if error:
            return error
        nha_phan_phoi.email = email

    if ds_san_pham is not None:
        list_sp_npp = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id = id).all()
        san_pham_ids = [sp_npp.san_pham_id for sp_npp in list_sp_npp]

        for san_pham in ds_san_pham:
            san_pham_id = san_pham.get("id")
            status = san_pham.get("status")
            if san_pham_id in san_pham_ids:
                product_npp = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id=id, san_pham_id=san_pham_id).first()
                if status is False:
                    product_npp.soft_delete()
                else:
                    product_npp.restore()
            elif status is True:
                sp_npp = SanPhamNhaPhanPhoi(nha_phan_phoi_id=id, san_pham_id=san_pham_id)
                db.session.add(sp_npp)

    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def delete_nha_phan_phoi(id):
    nha_phan_phoi = NhaPhanPhoi.query.get(id)

    if nha_phan_phoi is None:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)
    
    nha_phan_phoi.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)