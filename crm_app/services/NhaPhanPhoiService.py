from flask import make_response 
from crm_app.docs.containts import ERROR_CODES
from crm_app.services.utils import *
from crm_app.services.dbService import *
from crm_app.services.SanPhamService import delete_san_pham
from crm_app.models.NhaPhanPhoi import NhaPhanPhoi 
from crm_app.models.SanPham import SanPham 
from crm_app.models.SanPhamNhaPhanPhoi import SanPhamNhaPhanPhoi
from crm_app.models.HoaDonNhapKho import HoaDonNhapKho

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
            result = add_san_pham_nha_phan_phoi(nha_phan_phoi_id=new_nha_phan_phoi.id, san_pham_id=san_pham_id)

            if result is False:
                return result

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
        list_sp_npp = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id = id, deleted_at = None).all()
        san_pham_ids = [sp_npp.san_pham_id for sp_npp in list_sp_npp]

        for san_pham in ds_san_pham:
            san_pham_id = san_pham.get("id")
            status = san_pham.get("status")
            if san_pham_id in san_pham_ids:
                product_npp = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id=id, san_pham_id=san_pham_id).first()
                if status is False:
                    product_npp.soft_delete()
                else:
                    #Trường hợpp có sản phẩm id và nhà phân phôi id trong bảng <sản phẩm nhà phân phối> nhưng vẫn trả về true thì sẽ bỏ qua và k xử lý gì
                    pass
            elif status is True:
                result = add_san_pham_nha_phan_phoi(nha_phan_phoi_id=id, san_pham_id=san_pham_id)
                if result is False:
                    return result

    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def delete_nha_phan_phoi(id):
    nha_phan_phoi = NhaPhanPhoi.query.get(id)

    if nha_phan_phoi is None:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)
    
    error_response = check_reference_existence(model=HoaDonNhapKho, column_name='nha_phan_phoi_id', value=id, error_code=ERROR_CODES.NHA_PHAN_PHOI_REFERENCE_HOA_DON_NHAP)
    if error_response:
        return error_response
    
    error_response = check_reference_existence(model=SanPhamNhaPhanPhoi, column_name='nha_phan_phoi_id', value=id, error_code=ERROR_CODES.NHA_PHAN_PHOI_REFERENCE_HOA_DON_NHAP)
    if error_response:
        return error_response
    else:
        success = delete_san_pham_by_nha_phan_phoi(nha_phan_phoi_id=id)
        if not success:
            return success

    nha_phan_phoi.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)


def add_san_pham_nha_phan_phoi(nha_phan_phoi_id, san_pham_id):
    if isExistId(id=san_pham_id, model=SanPham):
        sp_npp = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id=nha_phan_phoi_id, san_pham_id=san_pham_id, deleted_at=None)
                        
        if sp_npp:
            return make_response(get_error_response(ERROR_CODES.SAN_PHAM_OF_NHA_PHAN_PHOI_EXISTED),401)

        san_pham_nha_phan_phoi = SanPhamNhaPhanPhoi(nha_phan_phoi_id=nha_phan_phoi_id, san_pham_id=san_pham_id)

        db.session.add(san_pham_nha_phan_phoi)
        return True
    
    return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND),401)

def delete_san_pham_by_nha_phan_phoi(nha_phan_phoi_id):
    san_phams = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id=nha_phan_phoi_id, deleted_at = None).all()

    for san_pham in san_phams:
        san_pham_id = san_pham.get("id")

        response = delete_san_pham(id=san_pham_id)
        if not response.status_code  == 200:
            print(f"Xóa sản phẩm {san_pham_id} thất bại!")
            return response
        
    return True