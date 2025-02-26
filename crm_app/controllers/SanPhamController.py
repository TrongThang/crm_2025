from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.SanPhamService import *
from crm_app.services.helpers import *

class SanPhamController(Resource):
    # @swag_from('')
    def get(self):
        data = request.get_json()
        skip = data.get('skip')
        take = data.get('take')
        sort = data.get('sort')
        order = data.get('order')
        filter = data.get('filter')

        result = get_san_pham(skip=skip, take=take, sort=sort, order=order, filter=filter)
        return result
    
    def post(self):
        file = request.files.get('file')
        data = request.form
        ten = data.get('ten')
        upc = data.get('upc')
        vat = data.get('vat')
        mo_ta = data.get('mo_ta')
        trang_thai = data.get('trang_thai')
        loai_id = data.get('loai_id')
        dvt_id = data.get('dvt_id')
        gg_id = data.get('gg_id')
        bh_id = data.get('bh_id')

        ten_pl = data.getlist('ten_pl')
        file_pl = request.files.getlist('file_pl')
        gia_nhap = data.getlist('gia_nhap')
        gia_ban = data.getlist('gia_ban')
        so_luong = data.getlist('so_luong')
        trang_thai_pl = data.getlist('trang_thai_pl')

        result = post_san_pham(ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, file=file, loai_id=loai_id, dvt_id=dvt_id, gg_id=gg_id, bh_id=bh_id, ten_pl=ten_pl, file_pl=file_pl, gia_nhap=gia_nhap, gia_ban=gia_ban, so_luong=so_luong, trang_thai_pl=trang_thai_pl)
        return result 

    def put(self):
        file = request.files.get('file')
        data = request.form
        id = data.get('id')
        ten = data.get('ten')
        upc = data.get('upc')
        vat = data.get('vat')
        mo_ta = data.get('mo_ta')
        trang_thai = data.get('trang_thai')
        loai_id = data.get('loai_id')
        dvt_id = data.get('dvt_id')
        gg_id = data.get('gg_id')
        bh_id = data.get('bh_id')
        
        id_pl = data.getlist('id_pl')
        ten_pl = data.getlist('ten_pl')
        file_pl = request.files.getlist('file_pl')
        gia_nhap = data.getlist('gia_nhap')
        gia_ban = data.getlist('gia_ban')
        so_luong = data.getlist('so_luong')
        trang_thai_pl = data.getlist('trang_thai_pl')

        result = put_san_pham(id=id, ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, file=file, loai_id=loai_id, dvt_id=dvt_id, gg_id=gg_id, bh_id=bh_id, id_pl=id_pl, ten_pl=ten_pl, file_pl=file_pl, gia_nhap=gia_nhap, gia_ban=gia_ban, so_luong=so_luong, trang_thai_pl=trang_thai_pl)

        return result

    def delete(self):
        data = request.get_json()
        id = data.get('id')
        id_ct = data.get('id_ct')
        id_pl = data.get('id_pl')

        if id_ct or id_pl:
            result = delete_chi_tiet_san_pham(id_ct=id_ct, id_pl=id_pl)
        elif id:
            result = delete_san_pham(id=id)
        return result

class ChiTietSanPhamController(Resource):
    # @swag_from('')
    def get(self):
        pass
    
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
