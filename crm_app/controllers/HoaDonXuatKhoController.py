from flask_restful import Resource
from flask import request
from flasgger import swag_from
from crm_app.services.HoaDonXuatKhoService import *
from crm_app.services.ChiTietXuatKhoService import *
from crm_app.services.CongNoService import get_cong_no_khach_hang
from crm_app import app

class HoaDonXuatKhoController(Resource):
    @app.route('/api/hoa-don-xuat-kho/cong-no')
    def get_cong_no():
        data    = request.args
        limit   = data.get("limit")
        page    = data.get("page")
        sort    = data.get("sort")
        order   = data.get("order")
        
        result  = get_cong_no_khach_hang(limit=limit, page=page, sort=sort, order=order) 

        return result
    
    @swag_from('../docs/swaggers/hd_xuat_kho/get_hd_xuat_kho.yaml')
    def get(seft):
        data    = request.args
        filters = data.get("filters")
        page    = data.get("page")
        limit   = data.get("limit")
        sort    = data.get("sort")
        order   = data.get("order")
        
        result  = get_hoa_don_xuat_kho(filter=filters, limit=limit, page=page, sort=sort, order=order) 

        return result
    
    @swag_from('../docs/swaggers/hd_xuat_kho/post_hd_xuat_kho.yaml')
    def post(seft):
        data = request.get_json()

        khach_hang_id          = data.get("khach_hang_id")
        nhan_vien_giao_hang_id = data.get("nhan_vien_giao_hang_id")
        nhan_vien_sale_id      = data.get("nhan_vien_sale_id")
        ngay_xuat              = data.get("ngay_xuat")
        tong_tien              = data.get("tong_tien")
        thanh_tien             = data.get("thanh_tien")
        tra_truoc              = data.get("tra_truoc")
        vat                    = data.get("vat")
        tong_gia_nhap          = data.get("tong_gia_nhap")
        loi_nhuan              = data.get("loi_nhuan")
        loai_chiet_khau        = data.get("loai_chiet_khau")
        gia_tri_chiet_khau     = data.get("gia_tri_chiet_khau")
        da_giao_hang           = data.get("da_giao_hang")
        ghi_chu                = data.get("ghi_chu")
        ds_san_pham_xuat       = data.get("ds_san_pham_xuat")

        result                 = post_hoa_don_xuat_kho(
            khach_hang_id=khach_hang_id, nv_giao_hang_id=nhan_vien_giao_hang_id, nv_sale_id=nhan_vien_sale_id, ngay_xuat=ngay_xuat, tong_tien=tong_tien, thanh_tien=thanh_tien, tra_truoc=tra_truoc, vat=vat, tong_gia_nhap=tong_gia_nhap, loi_nhuan=loi_nhuan, loai_chiet_khau=loai_chiet_khau, gia_tri_chiet_khau=gia_tri_chiet_khau, ghi_chu=ghi_chu, da_giao_hang=da_giao_hang, ds_san_pham_xuat=ds_san_pham_xuat
        )
        #khach_hang_id, nv_giao_hang_id, nv_sale_id, ngay_xuat, tong_tien, vat,thanh_tien, tra_truoc, tong_gia_nhap, loi_nhuan, ghi_chu, da_giao_hang, loai_chiet_khau, gia_tri_chiet_khau, ds_san_pham_xuat

        return result
    
    def put(seft):
        data                    = request.get_json()
        hoa_don_id              = data.get("hoa_don_id")
        khach_hang_id           = data.get("khach_hang_id")
        nhan_vien_giao_hang_id  = data.get("nhan_vien_giao_hang_id")
        nhan_vien_sale_id       = data.get("nhan_vien_sale_id")
        ngay_xuat               = data.get("ngay_xuat")
        vat                     = data.get("vat")
        tra_truoc               = data.get("tra_truoc")
        ghi_chu                 = data.get("ghi_chu")
        da_giao_hang            = data.get("da_giao_hang")
        loai_chiet_khau         = data.get("loai_chiet_khau")
        gia_tri_chiet_khau      = data.get("gia_tri_chiet_khau")
        khoa_don                = data.get("khoa_don")

        result = put_hoa_don_xuat_kho(hoa_don_id=hoa_don_id, khach_hang_id=khach_hang_id, nv_giao_hang_id=nhan_vien_giao_hang_id, nv_sale_id=nhan_vien_sale_id, ngay_xuat=ngay_xuat, vat=vat, tra_truoc=tra_truoc, ghi_chu=ghi_chu, da_giao_hang=da_giao_hang, loai_chiet_khau=loai_chiet_khau, gia_tri_chiet_khau=gia_tri_chiet_khau, khoa_don=khoa_don)
        return result
    
    def patch(seft):
        data                    = request.get_json()
        hoa_don_id              = data.get("hoa_don_id")
        khoa_don                = data.get("khoa_don")

        result = patch_lock(hoa_don_id=hoa_don_id, khoa_don=khoa_don)
        return result
    
class ChiTietXuatKhoController(Resource):
    
    def get(seft):
        id     = request.args.get("id")
        result = get_chi_tiet_xuat_kho(id)

        return result