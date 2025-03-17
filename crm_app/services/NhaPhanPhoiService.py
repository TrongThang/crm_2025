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
def config_data_nha_phan_phoi(data):
    merged_data = {}

    for item in data:
        key = item["ID"]  # Dùng ID để nhóm dữ liệu
        
        if key not in merged_data:
            # Nếu chưa có, tạo mới object
            merged_data[key] = {
                "CreatedAt": item["CreatedAt"],
                "DeletedAt": item["DeletedAt"],
                "ID": item["ID"],
                "ten": item["ten"],
                "UpdatedAt": item["UpdatedAt"],
                "dia_chi": item["dia_chi"],
                "dien_thoai": item["dien_thoai"],
                "email": item["email"],
                "ds_san_pham": []  # Danh sách sản phẩm
            }
        
        # Thêm sản phẩm vào danh sách
        merged_data[key]["ds_san_pham"].append({
            "ID": item.get("san_pham_id"),
            "upc": item.get("upc"),
            "ten": item.get("san_pham"),
            "don_vi_tinh": item.get("don_vi_tinh")
        })
        # merged_data[key]["san_pham"].append(item.get("upc"))

    result = list(merged_data.values())

    return result

def get_nha_phan_phoi(filter, limit, page, sort, order):
    get_table = 'nha_phan_phoi'
    get_attr = 'nha_phan_phoi.ten, dia_chi, dien_thoai, email, san_pham.upc, san_pham.ten as san_pham, san_pham.id as san_pham_id, don_vi_tinh.ten as don_vi_tinh'
    query_join = """
        LEFT JOIN san_pham_nha_phan_phoi ON san_pham_nha_phan_phoi.nha_phan_phoi_id = nha_phan_phoi.id AND san_pham_nha_phan_phoi.deleted_at IS NULL
        LEFT JOIN san_pham ON san_pham_nha_phan_phoi.san_pham_id = san_pham.id
        LEFT JOIN don_vi_tinh ON don_vi_tinh.id = san_pham.don_vi_tinh_id
    """
    
    result = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order,query_join=query_join)

    data_config = config_data_nha_phan_phoi(data = result.get("data"))

    response_data = {"data": data_config, "total_page":result.get("total_page")}
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
        for san_pham_id in ds_san_pham:
            result = add_san_pham_nha_phan_phoi(nha_phan_phoi_id=new_nha_phan_phoi.id, san_pham_id=san_pham_id)

            if result is not True:
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
        
        # [1, 3, 4, 6, 8]
        san_pham_ids = [sp_npp.san_pham_id for sp_npp in list_sp_npp]

        for san_pham_id in ds_san_pham:
            if not isExistId(id=san_pham_id, model=SanPham):
                return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND),401) 
            
            if san_pham_id not in san_pham_ids:
                result = add_san_pham_nha_phan_phoi(nha_phan_phoi_id=id, san_pham_id=san_pham_id)
                if result is not True:
                    return result
                san_pham_ids.append(san_pham_id) # [1, 3, 4, 6, 8, 9]
        # Ban đầu [1, 3, 4, 6, 8] -> Client gửi về -> 3 5 9 ->  Mất 1, 4, 6, 8 
        # MỚI 3 5 -> [3, 5, 9]
        # [1, 3, 4, 6, 8, 9] - [3, 5, 9] = [1, 4, 6, 8] (những thằng bị xoá)
        san_pham_delete = san_pham_ids - ds_san_pham

        for san_pham_id in san_pham_delete:
            if not isExistId(id=san_pham_id, model=SanPham):
                return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND),401)  
            sp_npp = SanPhamNhaPhanPhoi.query.filter_by().first()
            sp_npp.soft_delete()

    db.session.commit()
    return get_error_response(ERROR_CODES.SUCCESS)

def add_san_pham_nha_phan_phoi(nha_phan_phoi_id, san_pham_id):
    if isExistId(id=san_pham_id, model=SanPham):
        sp_npp = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id=nha_phan_phoi_id, san_pham_id=san_pham_id, deleted_at=None).first()
                        
        # if not sp_npp:
        #     return make_response(get_error_response(ERROR_CODES.SAN_PHAM_OF_NHA_PHAN_PHOI_EXISTED),401)

        san_pham_nha_phan_phoi = SanPhamNhaPhanPhoi(nha_phan_phoi_id=nha_phan_phoi_id, san_pham_id=san_pham_id)

        db.session.add(san_pham_nha_phan_phoi)
        return True
    
    print('đã có sản phẩm')
    return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND),401)

def delete_nha_phan_phoi(id):
    nha_phan_phoi = NhaPhanPhoi.query.get(id)

    if nha_phan_phoi is None:
        return make_response(get_error_response(ERROR_CODES.NHA_PHAN_PHOI_NOT_FOUND), 401)
    
    error_response = check_reference_existence(model=HoaDonNhapKho, column_name='nha_phan_phoi_id', value=id, error_code=ERROR_CODES.NHA_PHAN_PHOI_REFERENCE_HOA_DON_NHAP)
    if error_response:
        return error_response
    
    error_response = check_reference_existence(model=SanPhamNhaPhanPhoi, column_name='nha_phan_phoi_id', value=id, error_code=ERROR_CODES.NHA_PHAN_PHOI_REFERENCE_SAN_PHAM)
    if error_response:
        return error_response
    else:
        success = delete_san_pham_by_nha_phan_phoi(nha_phan_phoi_id=id)
        if not success:
            return success

    nha_phan_phoi.soft_delete()

    return get_error_response(ERROR_CODES.SUCCESS)



def delete_san_pham_by_nha_phan_phoi(nha_phan_phoi_id):
    san_phams = SanPhamNhaPhanPhoi.query.filter_by(nha_phan_phoi_id=nha_phan_phoi_id, deleted_at = None).all()

    for san_pham in san_phams:
        san_pham_id = san_pham.get("id")

        response = delete_san_pham(id=san_pham_id)
        if not response.status_code  == 200:
            print(f"Xóa sản phẩm {san_pham_id} thất bại!")
            return response
        
    return True