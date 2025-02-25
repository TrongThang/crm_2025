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
            "id": row["sp_id"],
            "ten": row["sp_ten"],
            "upc": row["upc"],
            "hinh_anh": row["sp_hinh_anh"],
            "vat": row["vat"],
            "mo_ta": (
                row["sp_mo_ta"].decode('utf-8', errors='replace')
                if isinstance(row["sp_mo_ta"], bytes)
                else row["sp_mo_ta"]
            ),
            "trang_thai": row["sp_trang_thai"],
            "loai_san_pham": {"id": row["lsp_id"], "ten": row["lsp_ten"]} if row["lsp_id"] else None,
            "don_vi_tinh": {"id": row["dvt_id"], "ten": row["dvt_ten"]} if row["dvt_id"] else None,
            "loai_giam_gia": {"id": row["gg_id"], "ten": row["gg_ten"]} if row["gg_id"] else None,
            "thoi_gian_bao_hanh": {"id": row["bh_id"], "ten": row["bh_ten"]} if row["bh_id"] else None,
            "created_at": str(row["created_at"]),  # Chuyển datetime thành string
            "updated_at": str(row["updated_at"]),
            "deleted_at": str(row["deleted_at"]) if row["deleted_at"] else None
        }
        for row in result_set
    ]

    return result_list

def get_san_pham (ten=None, mota=None, vat=None, lsp=None, dvt=None, gg=None, bh=None):
    ten = f"%{ten}" if ten else "%"
    mota = f"%{mota}" if mota else "%"
    vat = f"%{vat}" if vat else "%"
    lsp = f"%{lsp}" if lsp else "%"
    dvt = f"%{dvt}" if dvt else "%"
    gg = f"%{gg}" if gg else "%"
    bh = f"%{bh}" if bh else "%"

    query = text("""
    SELECT 
        sp.id as sp_id, sp.ten as sp_ten, upc, sp.hinh_anh as sp_hinh_anh, vat,
            mo_ta as sp_mo_ta, trang_thai as sp_trang_thai, 
        lsp.id as lsp_id, lsp.ten as lsp_ten, dvt.id as dvt_id, dvt.ten as dvt_ten, 
        gg.id as gg_id, gg.ten as gg_ten, bh.id as bh_id, bh.ten as bh_ten, 
        sp.created_at, sp.updated_at, sp.deleted_at 
    FROM san_pham sp 
        LEFT JOIN 
            loai_san_pham lsp ON lsp.id = sp.loai_san_pham_id
        LEFT JOIN 
            don_vi_tinh dvt ON dvt.id = sp.don_vi_tinh_id
        LEFT JOIN 
            loai_giam_gia gg ON gg.id = sp.loai_giam_gia_id
        LEFT JOIN
            thoi_gian_bao_hanh bh ON bh.id = sp.thoi_gian_bao_hanh_id
    WHERE sp.ten LIKE :ten
        OR sp.mo_ta LIKE :mota 
        OR sp.vat LIKE :vat
        OR lsp.ten LIKE :lsp_ten
        OR dvt.ten LIKE :dvt_ten
        OR gg.ten LIKE :gg_ten
        OR bh.ten LIKE :bh_ten
                """)
    result_set  = db.session.execute(query,{
        'ten':ten,
        'mota':mota,
        'vat':vat,
        'lsp_ten':lsp,
        'dvt_ten':dvt,
        'gg_ten':gg,
        'bh_ten':bh,
    }).mappings().all()

    
    result_list = to_dict(result_set=result_set)

    return get_error_response(ERROR_CODES.SUCCESS, result=result_list)

def post_san_pham (ten=None, upc=None, vat=None, mo_ta=None, trang_thai=None, file = None, loai_id=None, dvt_id=None, gg_id=None, bh_id=None, ):
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
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def put_san_pham (id = None, ten=None, upc=None, vat=None, mo_ta=None, trang_thai=None, file = None, loai_id=None, dvt_id=None, gg_id=None, bh_id=None):
    san_pham = SanPham.query.get(id)
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
        isExisted = isExistId(dvt_id, LoaiSanPham)
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
    
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)

def delete_san_pham(id):
    sp_delete = SanPham.query.get(id)

    if sp_delete is None:
        return get_error_response(ERROR_CODES.SAN_PHAM_NOT_FOUND)
    
    db.session.delete(sp_delete)
    db.session.commit()

    return get_error_response(ERROR_CODES.SUCCESS)