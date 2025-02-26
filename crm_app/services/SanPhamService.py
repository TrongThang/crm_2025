from flask import jsonify
from crm_app.docs.containts import ERROR_CODES, MESSAGES
from crm_app.services.utils import *
from crm_app.models.SanPham import SanPham
from crm_app.models.DonViTinh import DonViTinh
from crm_app.models.LoaiSanPham import LoaiSanPham
from crm_app.models.BaoHanh import BaoHanh
from crm_app.models.GiamGia import GiamGia
from crm_app import db
from sqlalchemy import text
import json
from crm_app.services.helpers import *

from crm_app.services.ChiTietSanPhamService import *

def to_dict_test(self):
    result = {}
    for key, value in self.__dict__.items():
        if isinstance(value, bytes):
            result[key] = value.decode("utf-8", errors="replace")
        elif isinstance(value, datetime):
            result[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        else:
            result[key] = value
    return result

def to_dict(result_set):
    result_list = [
        {
            "id": row["id"],
            "ten": row["ten"],
            "upc": row["upc"],
            "hinh_anh": row["hinh_anh"],
            "vat": row["vat"],
            "mo_ta": (
                row["mo_ta"].decode('utf-8', errors='replace')
                if isinstance(row["mo_ta"], bytes)
                else row["mo_ta"]
            ),
            "trang_thai": row["trang_thai"],
            "loai_san_pham_id": row["loai_san_pham_id"],
            "loai_san_pham": row["loai_san_pham"],
            "don_vi_tinh_id": row["don_vi_tinh_id"],
            "don_vi_tinh": row["don_vi_tinh"],
            "loai_giam_gia_id": row["loai_giam_gia_id"],
            "loai_giam_gia": row["loai_giam_gia"],
            "thoi_gian_bao_hanh_id": row["thoi_gian_bao_hanh_id"],
            "thoi_gian_bao_hanh": row["thoi_gian_bao_hanh"],

            "created_at": str(row["created_at"]),
            "updated_at": str(row["updated_at"]),
            "deleted_at": str(row["deleted_at"]) if row["deleted_at"] else None
        }
        for row in result_set
    ]

    return result_list

def get_san_pham (skip, take, sort, order, filter):
    build_where = build_where_query(filter=filter) if filter else ''

    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {sort} {opt_order} " if sort else ""
    
    print("build_sort:", build_sort) 

    query = text(f"""
    SELECT 
        san_pham.id as id, san_pham.ten as ten, upc, san_pham.hinh_anh as hinh_anh, vat, mo_ta as mo_ta, trang_thai, 
        loai_san_pham.id as loai_san_pham_id, loai_san_pham.ten as loai_san_pham, don_vi_tinh.id as don_vi_tinh_id, don_vi_tinh.ten as don_vi_tinh, 
        loai_giam_gia.id as loai_giam_gia_id, loai_giam_gia.ten as loai_giam_gia, thoi_gian_bao_hanh.id as thoi_gian_bao_hanh_id, thoi_gian_bao_hanh.ten as thoi_gian_bao_hanh, 
        san_pham.created_at, san_pham.updated_at, san_pham.deleted_at 
    FROM san_pham 
        LEFT JOIN 
            loai_san_pham ON loai_san_pham.id = san_pham.loai_san_pham_id
        LEFT JOIN   
            don_vi_tinh ON don_vi_tinh.id = san_pham.don_vi_tinh_id
        LEFT JOIN 
            loai_giam_gia ON loai_giam_gia.id = san_pham.loai_giam_gia_id
        LEFT JOIN
            thoi_gian_bao_hanh ON thoi_gian_bao_hanh.id = san_pham.thoi_gian_bao_hanh_id
    {build_where} 
    {build_sort} 
    LIMIT {take} 
    OFFSET {skip} 
                """)
    result_set = db.session.execute(query).mappings().all()

    result_list = to_dict(result_set=result_set)

    return get_error_response(ERROR_CODES.SUCCESS, result=result_list)

def post_san_pham (ten, upc, vat, mo_ta, trang_thai, file, loai_id, dvt_id, gg_id, bh_id, 
ten_pl, file_pl, gia_nhap, gia_ban, so_luong, trang_thai_pl):
    error = validate_name(name=ten, model=SanPham)
    if error:
        return error
    
    error = validate_name(name=upc, model=SanPham)
    if error:
        return error
    
    error = validate_number(number=vat, model=SanPham)
    if error:
        return error
    
    upload = save_uploaded_file(file, "san_pham", prefix='san_pham_')
    if upload['errorCode'] == ERROR_CODES.SUCCESS:
        filename = upload['filename']
    elif (upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND):
        filename = None
    else:
        return get_error_response(upload['errorCode'])
    
    san_pham = SanPham(ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, hinh_anh = filename, loai_san_pham_id=loai_id, don_vi_tinh_id=dvt_id, loai_giam_gia_id=gg_id, thoi_gian_bao_hanh_id=bh_id)

    db.session.add(san_pham)
    db.session.flush()
    for ten_ct, file_ct, nhap, ban, soluong in zip(ten_pl, file_pl, gia_nhap, gia_ban, so_luong):
        result_ct = add_chi_tiet_san_pham(
            san_pham_id=san_pham.id, 
            ten_phan_loai=ten_ct,  
            file_phan_loai=file_ct,  
            gia_nhap=nhap,  
            gia_ban=ban,  
            so_luong=soluong,  
            trang_thai_pl=san_pham.trang_thai
        )

        if isinstance(result_ct, dict) and result_ct.get('errorCode') != ERROR_CODES.SUCCESS:  
            return result_ct
        
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def put_san_pham (id, ten, upc, vat, mo_ta, trang_thai, file, loai_id, dvt_id, gg_id, bh_id,
                id_pl, ten_pl, file_pl, gia_nhap, gia_ban, so_luong, trang_thai_pl
                ):
    san_pham = SanPham.query.get(id)
    print('san_pham:', san_pham.id)
    print('san_pham:', san_pham.ten)
    if san_pham is None:
        return get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND)
    
    if ten is not None:
        error = validate_name(name=ten, model=SanPham)
        if error:
            return error
        san_pham.ten = ten
    
    if upc is not None:
        error = validate_name(name=upc, model=SanPham)
        if error:
            return error
        san_pham.upc = upc
    
    if vat is not None:
        error = validate_number(number=vat, model=SanPham)
        if error:
            return error
        san_pham.vat = vat

    if mo_ta is not None:
        san_pham.mo_ta = mo_ta
    if trang_thai is not None:
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
            
    if file is not None:
        upload = save_uploaded_file(file, "san_pham", prefix='san_pham_')
        if upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND:
            filename = upload['filename']
        elif (upload['errorCode'] == ERROR_CODES.FILE_NOT_FOUND):
            filename = None
        else:
            return get_error_response(upload['errorCode'])
    
    for id, ten_ct, file_ct, nhap, ban, soluong in zip(id_pl, ten_pl, file_pl, gia_nhap, gia_ban, so_luong):
        result_ct = update_chi_tiet_san_pham(
            id=id,
            san_pham_id=san_pham.id, 
            ten_phan_loai=ten_ct,  
            file_phan_loai=file_ct,  
            gia_nhap=nhap,  
            gia_ban=ban,  
            so_luong=soluong,  
            trang_thai_pl=san_pham.trang_thai
        )

        if isinstance(result_ct, dict) and result_ct.get('errorCode') != ERROR_CODES.SUCCESS:  
            return result_ct
        
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_san_pham(id):
    sp_delete = SanPham.query.get(id)

    if sp_delete is None:
        return get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND)
    
    result_ct = delete_many_chi_tiet_san_pham(san_pham_id=id)

    # if isinstance(result_ct, dict) and result_ct.get('errorCode') != ERROR_CODES.SUCCESS: 
    delete_file(upload_folder="san_pham",filename=sp_delete.hinh_anh)
    db.session.delete(sp_delete)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_chi_tiet_san_pham(id_ct = None, id_pl = None):
    if id_pl is not None:
        for id in id_pl:
            ct_delete = ChiTietSanPham.query.get(id)
            if ct_delete is None:
                return get_error_response(ERROR_CODES.CTSP_INVALID_ID)
            db.session.delete(ct_delete)
    elif id_ct is not None:
        ct_delete = ChiTietSanPham.query.get(id_ct)
        if ct_delete is None:
            return get_error_response(ERROR_CODES.CTSP_INVALID_ID)
        delete_file(upload_folder="chi_tiet_sp",filename=ct_delete.hinh_anh)
        db.session.delete(ct_delete)
    
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)