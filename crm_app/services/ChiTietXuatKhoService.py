from crm_app.services.dbService import excute_select_data 
from crm_app.docs.containts import ERROR_CODES, get_error_response
from crm_app import db
from sqlalchemy import text
def get_chi_tiet_xuat_kho(id):
    query = text("""
        SELECT 
            chi_tiet_hoa_don_xuat_kho.id, hoa_don_id, chi_tiet_hoa_don_xuat_kho.san_pham_id, ctsp_id, lo, 
            chi_tiet_hoa_don_xuat_kho.so_luong as so_luong_xuat, don_vi_tinh, 
            chi_tiet_hoa_don_xuat_kho.gia_ban as gia_xuat, chiet_khau, thanh_tien, la_qua_tang
        FROM chi_tiet_hoa_don_xuat_kho
            LEFT JOIN san_pham ON san_pham_id = san_pham.id
            LEFT JOIN chi_tiet_san_pham ON ctsp_id = chi_tiet_san_pham.id
        WHERE
            chi_tiet_hoa_don_xuat_kho.id = :id
    """)
    data = db.session.execute(query, {"id": id}).mappings().first()

    result = dict(data.items()) 
    
    return get_error_response(ERROR_CODES.SUCCESS, result=result)