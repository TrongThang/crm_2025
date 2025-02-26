from crm_app.services.utils import *
from crm_app.services.helpers import *
from crm_app.models.NhanVien import NhanVien
from crm_app.models.ChucVu import ChucVu

from crm_app import db
def get_nhan_vien(filter):
    build_where = build_where_query(filter=filter)
    query = text(f"""SELECT 
                        nhan_vien.id, ho_ten, email, dien_thoai, dia_chi, avatar, cv.ten as chuc_vu, cv.id as chuc_vu_id, nhan_vien.created_at, nhan_vien.updated_at, nhan_vien.deleted_at
                    FROM nhan_vien
                        LEFT JOIN chuc_vu cv ON cv.id = nhan_vien.id
                    {build_where}
                """)
    data = db.session.execute(query).fetchall()

    result = [{
        'id': row.id,
        'ho_ten': row.ho_ten,
        'email': row.email,
        'dien_thoai': row.dien_thoai,
        'dia_chi': row.dia_chi,
        'avatar': row.avatar,
        'chuc_vu_id': row.avatar,
        'chuc_vu': row.chuc_vu,
        'created_at': row.created_at,
        'updated_at': row.updated_at,
        'deleted_at': row.deleted_at,
    }
    for row in data
    ]

    return get_error_response(ERROR_CODES.SUCCESS, data)

def post_nhan_vien(ho_ten, email, dien_thoai, avatar, chuc_vu_id):
    error = validate_name(ho_ten)
    if error:
        return error
    
    error = validate_email(email)
    if error:
        return error

    error = validate_phone(dien_thoai)
    if error:
        return error
    
    upload = save_uploaded_file(avatar, "nhan_vien", prefix="nhan_vien_")
    if upload['errorCode'] == ERROR_CODES.SUCCESS:
        filename = upload['filename']
    elif upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND:
        filename = None
    else:
        return get_error_response(upload['errorCode'])

    nhan_vien = NhanVien(ho_ten=ho_ten, email=email, dien_thoai=dien_thoai, avatar=filename, chuc_vu_id=chuc_vu_id)
    db.session.add(nhan_vien)
    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)


def put_nhan_vien(id, ho_ten, email, dien_thoai, avatar, chuc_vu_id):
    nhan_vien = NhanVien.query.get(id)
    if NhanVien is None:
        return get_error_response(ERROR_CODES.NHAN_VIEN_NOT_FOUND)
    if ho_ten is not None:
        if len(ho_ten) > 255 or len(ho_ten) <= 0:
            return get_error_response(ERROR_CODES.NHAN_VIEN_NAME_LENGTH) 
        nhan_vien.ho_ten = ho_ten
    if email is not None:
        error = validate_email(email=email)
        if error:
            return error
        
    if dien_thoai is not None:
        error = validate_phone(phone=dien_thoai)
        if error:
            return error

    if chuc_vu_id is not None:
        isExisted = isExistId(id=chuc_vu_id, model=ChucVu)
        if isExisted != True:
            return isExisted
        nhan_vien.chuc_vu_id = chuc_vu_id

    if avatar is not None:
        upload = save_uploaded_file(avatar,"nhan_vien", filename=nhan_vien.avatar, prefix="nhan_vien")
        if upload['errorCode'] == ERROR_CODES.SUCCESS:
            nhan_vien.avater = upload['filename']
        elif upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND:
            pass
        else:
            return get_error_response(upload['errorCode'])
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)


def delete_nhan_vien():

    return get_error_response(ERROR_CODES.SUCCESS)
