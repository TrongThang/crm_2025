from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.docs.formatContaints import STATUS, get_status_by_object
from crm_app.services.utils import *
from crm_app.models.SanPham import SanPham
from crm_app.models.DonViTinh import DonViTinh
from crm_app.models.LoaiSanPham import LoaiSanPham
from crm_app.models.BaoHanh import BaoHanh
from crm_app.models.GiamGia import GiamGia

from crm_app.models.SanPhamNhaPhanPhoi import SanPhamNhaPhanPhoi
from crm_app.models.ChiTietNhapKho import ChiTietNhapKho
from crm_app.models.ChiTietXuatKho import ChiTietXuatKho
from crm_app.models.TonKho import TonKho
from crm_app.models.ChiTietSanPham import ChiTietSanPham

from crm_app import db
from sqlalchemy import text
import json
from crm_app.services.helpers import *
from crm_app.services.dbService import *
from crm_app.services.ChiTietSanPhamService import *
from crm_app.services.utils import isExistId
import math 

def to_dict(result_set):
    result_list = [
        {
            "ID": row["ID"],
            "ten": row["ten"],
            "upc": row["upc"],
            "hinh_anh": row["hinh_anh"],
            "vat": row["vat"],
            "mo_ta": (
                row["mo_ta"].decode('utf-8', errors='replace')
                if isinstance(row["mo_ta"], bytes)
                else row["mo_ta"]
            ),
            "trang_thai": 'active' if row["trang_thai"] == 1 else 'inactive',
            "loai_san_pham_id": row["loai_san_pham_id"],
            "loai_san_pham": row["loai_san_pham"],
            "don_vi_tinh_id": row["don_vi_tinh_id"],
            "don_vi_tinh": row["don_vi_tinh"],
            "loai_giam_gia_id": row["loai_giam_gia_id"],
            "loai_giam_gia": row["loai_giam_gia"],
            "thoi_gian_bao_hanh_id": row["thoi_gian_bao_hanh_id"],
            "thoi_gian_bao_hanh": row["thoi_gian_bao_hanh"],

            "CreatedAt": str(row["CreatedAt"]),
            "UpdatedAt": str(row["UpdatedAt"]),
            "DeletedAt": str(row["DeletedAt"]) if row["DeletedAt"] else None
        }
        for row in result_set
    ]

    return result_list

def get_san_pham (limit, page, sort, order, filter):
    get_attr = text(f"""
        san_pham.ten as ten, upc, san_pham.hinh_anh as hinh_anh, CAST(mo_ta AS CHAR) AS mo_ta, vat, trang_thai, 
        loai_san_pham.id as loai_san_pham_id, loai_san_pham.ten as loai_san_pham, don_vi_tinh.id as don_vi_tinh_id, don_vi_tinh.ten as don_vi_tinh, 
        loai_giam_gia.id as loai_giam_gia_id, loai_giam_gia.ten as loai_giam_gia, thoi_gian_bao_hanh.id as thoi_gian_bao_hanh_id, thoi_gian_bao_hanh.ten as thoi_gian_bao_hanh
    """)
    get_table = "san_pham"
    query_join = text("""
        LEFT JOIN 
            loai_san_pham ON loai_san_pham.id = san_pham.loai_san_pham_id
        LEFT JOIN   
            don_vi_tinh ON don_vi_tinh.id = san_pham.don_vi_tinh_id
        LEFT JOIN 
            loai_giam_gia ON loai_giam_gia.id = san_pham.loai_giam_gia_id
        LEFT JOIN
            thoi_gian_bao_hanh ON thoi_gian_bao_hanh.id = san_pham.thoi_gian_bao_hanh_id
    """)
    # result_set = db.session.execute(query).mappings().all()

    # result_list = to_dict(result_set=result_set)
    # total_page = math.ceil(len(result_list)/limit)
    response_data = excute_select_data(table=get_table, str_get_column=get_attr, filter=filter, limit=limit, page=page, sort=sort, order=order, query_join=query_join)
    return get_error_response(ERROR_CODES.SUCCESS, result=response_data)

def post_san_pham (ten, upc, vat, mo_ta, trang_thai, hinh_anh, loai_id, dvt_id, gg_id, bh_id, chi_tiet_san_pham):
    try:
        print('thêm sản phẩm 1')
        
        error = validate_name(name=ten, model=SanPham)
        if error:
            return error
        
        existed = isExistId(loai_id, LoaiSanPham)
        if not existed:
            return make_response(get_error_response(ERROR_CODES.LOAI_SP_NOT_FOUND), 401)
        
        error = validate_name(name=upc, model=SanPham)
        if error:
            return error
        
        upc_existed = SanPham.query.filter_by(upc=upc).first()
        if upc_existed:
            return make_response(get_error_response(ERROR_CODES.SAN_PHAM_UPC_EXISTED), 401)
        
        error = validate_number(number=vat)
        if error:        return error
        print('vượt qua kiểm tra')
        
        san_pham = SanPham(ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, hinh_anh = hinh_anh, loai_san_pham_id=loai_id, don_vi_tinh_id=dvt_id, loai_giam_gia_id=gg_id, thoi_gian_bao_hanh_id=bh_id)
        print('trước thêm sản phẩm')

        db.session.add(san_pham)
        print('thêm sản phẩm thành công')

        db.session.flush()

        if len(chi_tiet_san_pham) > 0:
            for item in chi_tiet_san_pham:
                result_ct = add_chi_tiet_san_pham(
                    san_pham_id=san_pham.id, 
                    ten_phan_loai=item.get("ten_phan_loai"),  
                    file_phan_loai=item.get("hinh_anh"),  
                    # gia_nhap=item.nhap,  
                    # gia_ban=item.ban,  
                    # so_luong=item.soluong,  
                    trang_thai_pl= 1#item.get("trang_thai")
                )
                
                if isinstance(result_ct, dict) and result_ct.get('errorCode') != ERROR_CODES.SUCCESS:  
                    return result_ct
        else:
            print("trước thêm sản phẩm 0 phân loại")
            res = add_chi_tiet_san_pham(san_pham_id=san_pham.id, ten_phan_loai=None, trang_thai_pl=trang_thai)
            print("sau thêm sản phẩm 0 phân loại")
        print(123123123123)
        db.session.commit()
    except Exception as e:
        # db.session.rollback() 
        print("Lỗi:", e)
        return make_response(str(e), 500)
    
    finally:
        return get_error_response(ERROR_CODES.SUCCESS)

def put_san_pham (id, ten, upc, vat, mo_ta, trang_thai, hinh_anh, loai_id, dvt_id, gg_id, bh_id, chi_tiet_san_pham):
    san_pham = SanPham.query.get(id)
    print('san_pham:', san_pham.id)
    print('san_pham:', san_pham.ten)
    
    if san_pham is None:
        return get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND)
    
    if ten is not None:
        error = validate_name(name=ten, model=SanPham, existing_id=id)
        if error:
            return error
        san_pham.ten = ten
    
    if upc is not None:
        error = validate_name(name=upc, model=SanPham)
        if error:
            return error
        san_pham.upc = upc
    
    if vat is not None:
        error = validate_number(number=vat)
        if error:
            return error
        san_pham.vat = vat
    if hinh_anh is not None:
        san_pham.hinh_anh = hinh_anh
    if mo_ta is not None:
        san_pham.mo_ta = mo_ta
    if trang_thai is not None:
        # trang_thai = get_status_by_object(trang_thai)
        # if not trang_thai:
            # return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND_TRANG_THAI), 401)
        san_pham.trang_thai = trang_thai
    if loai_id is not None:
        isExisted = isExistId(loai_id, LoaiSanPham)
        if isExisted != True:
            return isExisted
        san_pham.loai_san_pham_id = loai_id
    if dvt_id is not None:
        isExisted = isExistId(dvt_id, DonViTinh)
        if isExisted != True:
            return isExisted
        san_pham.don_vi_tinh_id = dvt_id
    if gg_id is not None:
        isExisted = isExistId(gg_id, GiamGia)
        if isExisted != True:
            return isExisted
        san_pham.loai_giam_gia_id = gg_id
    if bh_id is not None:
        isExisted = isExistId(bh_id, BaoHanh)
        if isExisted != True:
            return isExisted
        san_pham.thoi_gian_bao_hanh_id = bh_id
    
    # Lấy danh sách ID chi tiết sản phẩm hiện tại trong database
    existing_ctsp_ids = {ctsp.id for ctsp in ChiTietSanPham.query.filter_by(san_pham_id=id, deleted_at=None).all()}

    # Danh sách ID chi tiết sản phẩm được gửi lên
    received_ctsp_ids = set()

    for item in chi_tiet_san_pham:
        print(item)
        ctsp_id = item.get("id")
        if ctsp_id == 0:        

            print("Thêm một chi tiết sản phấmr")
            result_ct = add_chi_tiet_san_pham(
                san_pham_id=san_pham.id, 
                ten_phan_loai=item.get("ten_phan_loai"),  
                file_phan_loai=item.get("hinh_anh"),  
                trang_thai_pl=item.get("trang_thai")
            )
        elif ctsp_id:
            received_ctsp_ids.add(ctsp_id)
            print("trạng thái:",item.get("trang_thai"))
            result_ct = update_chi_tiet_san_pham(
                id=item.get("id"),
                ten_phan_loai=item.get("ten_phan_loai"),  
                file_phan_loai=item.get("hinh_anh"),  
                trang_thai=item.get("trang_thai")
            )

        if isinstance(result_ct, dict) and result_ct.get('errorCode') != ERROR_CODES.SUCCESS:  
            return result_ct
        
    ids_to_delete = existing_ctsp_ids - received_ctsp_ids
    if ids_to_delete:
        for ctsp_id in ids_to_delete:
            response = delete_one_chi_tiet_san_pham(id=ctsp_id)
            if response.status_code != 200:
                return response
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def check_existed_product_by_model(model, errorCode:ERROR_CODES):
    if model.query.filter_by(san_pham_id=id, deleted_at=None):
        return make_response(get_error_response(error_code=errorCode), 401)
    
    return False

def delete_san_pham(id):
    sp_delete = SanPham.query.get(id)
    
    if sp_delete is None:
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND), 401)

    if SanPhamNhaPhanPhoi.query.filter_by(san_pham_id=id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_REFERENCE_NHA_PHAN_PHOI), 401)
    
    if TonKho.query.filter_by(san_pham_id=id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_REFERENCE_TON_KHO), 401)
    
    if ChiTietNhapKho.query.filter_by(san_pham_id=id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_REFERENCE_CHI_TIET_NHAP_HD), 401)
    
    if ChiTietXuatKho.query.filter_by(san_pham_id=id, deleted_at=None):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_REFERENCE_CHI_TIET_XUAT_HD), 401)
    
    if ChiTietSanPham.query.filter_by(san_pham_id=id, deleted_at=None,khong_phan_loai=False):
        return make_response(get_error_response(ERROR_CODES.SAN_PHAM_REFERENCE_CTSP), 401)
    
    result_ct = delete_many_chi_tiet_san_pham(san_pham_id=id)

    # if isinstance(result_ct, dict) and result_ct.get('errorCode') != ERROR_CODES.SUCCESS: 
    # delete_file(upload_folder="san_pham",filename=sp_delete.hinh_anh)
    sp_delete.soft_delete()
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)
