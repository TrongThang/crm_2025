from flask_restful import Resource
from flask import request
from crm_app.services.HoaDonXuatKhoService import *
from crm_app.services.ChiTietXuatKhoService import *

class HoaDonXuatKhoController(Resource):
    def get(seft):
        data = request.args
        filters = data.get("filters")
        page = data.get("page")
        limit = data.get("limit")
        sort = data.get("sort")
        order = data.get("order")
        
        result = get_hoa_don_xuat_kho(filter=filters, limit=limit, page=page, sort=sort, order=order) 

        return result
    
    def post(seft):
        data = request.get_json()

        khach_hang_id = data.get("khach_hang_id")
        nhan_vien_giao_hang_id = data.get("nhan_vien_giao_hang_id")
        nhan_vien_sale_id = data.get("nhan_vien_sale_id")
        ngay_xuat = data.get("ngay_xuat")
        thanh_tien = data.get("thanh_tien")
        tra_truoc = data.get("tra_truoc")
        ghi_chu = data.get("ghi_chu")
        ds_san_pham_xuat = data.get("ds_san_pham_xuat")

        result = post_hoa_don_xuat_kho(khach_hang_id=khach_hang_id, nhan_vien_giao_hang_id=nhan_vien_giao_hang_id, nhan_vien_sale_id=nhan_vien_sale_id, ngay_xuat=ngay_xuat, thanh_tien=thanh_tien, tra_truoc=tra_truoc, ghi_chu=ghi_chu, ds_san_pham_xuat=ds_san_pham_xuat)

        return result
    
class ChiTietXuatKhoController(Resource):
    def get(seft):
        id = request.args.get("id")
        result = get_chi_tiet_xuat_kho(id)

        return result