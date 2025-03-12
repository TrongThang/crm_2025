from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.HoaDonNhapKhoService import *

class HoaDonNhapKhoController(Resource):
    @swag_from('../docs/swaggers/hd_nhap_kho/get_hd_nhap_kho.yaml')
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')
        result = get_hoa_don_nhap_kho(filter, limit=limit, page=page, sort=sort, order=order)

        return result
    
    @swag_from('../docs/swaggers/hd_nhap_kho/post_hd_nhap_kho.yaml')
    def post(self):
        data = request.get_json()
        nha_phan_phoi_id = data.get('nha_phan_phoi_id')
        kho_id = data.get('kho_id')
        ngay_nhap = data.get('ngay_nhap')
        tong_tien = data.get('tong_tien')
        tra_truoc = data.get('tra_truoc')
        ghi_chu = data.get('ghi_chu')
        ds_san_pham_nhap = data.get('ds_san_pham_nhap')

        result = post_hoa_don_nhap_kho(nha_phan_phoi_id=nha_phan_phoi_id, kho_id=kho_id, ngay_nhap=ngay_nhap, tong_tien=tong_tien, tra_truoc=tra_truoc, ghi_chu=ghi_chu, ds_san_pham_nhap=ds_san_pham_nhap)
        return result

    # @swag_from('../docs/swaggers/hd_nhap_kho/put_hd_nhap_kho.yaml')

    # @swag_from('../docs/swaggers/hd_nhap_kho/delete_hd_nhap_kho.yaml')