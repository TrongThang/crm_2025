from crm_app.services.utils import *
from crm_app.services.helpers import build_where_query
from crm_app.services.dbService import excute_select_data
from crm_app.models.ChucVu import ChucVu
from crm_app.models.NhanVien import NhanVien
from crm_app import db

def get_chuc_vu(filter, limit, page, sort, order):
    get_attr = "chuc_vu.ten as ten"
    get_table = "chuc_vu"

    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order)

    return get_error_response(ERROR_CODES.SUCCESS, result=response_data)

def post_chuc_vu(ten):
    error = validate_name(name=ten, model=ChucVu)
    if error:   
        return error
    
    chuc_vu = ChucVu(ten=ten)

    db.session.add(chuc_vu)
    db.session.commit()
    return

def put_chuc_vu(id, ten):
    chuc_vu = ChucVu.query.get(id)
    if chuc_vu is None:
        return 
    error = validate_name(name=ten, model=ChucVu, existing_id=id)
    if error:
        return error
    chuc_vu.ten = ten

    db.session.commit()
    
    return get_error_response(ERROR_CODES.SUCCESS)


def delete_chuc_vu(id):
    chuc_vu = ChucVu.query.get(id)
    if chuc_vu is None:
        return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 406)
    
    nhan_vien = NhanVien.query.filter_by(chuc_vu_id = id)
    if nhan_vien:
        return make_response(str({"message": "Có nhân viên tham chiếu tới chức vụ này"}), 406)

    chuc_vu.soft_delete()
    return get_error_response(ERROR_CODES.SUCCESS)