from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.SanPhamService import *
from crm_app.services.helpers import *
from crm_app import app
from crm_app.services.ChiTietSanPhamService import *
class SanPhamController(Resource):
    @swag_from('../docs/swaggers/san_pham/get_san_pham.yaml')
    def get(self):
        data = request.args
        limit = data.get('limit')
        page = data.get('page')
        sort = data.get('sort')
        order = data.get('order')
        filter = data.get('filters')

        result = get_san_pham(limit=limit, page=page, sort=sort, order=order, filter=filter)
        return result
    
    @swag_from('../docs/swaggers/san_pham/post_san_pham.yaml')
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

    @swag_from('../docs/swaggers/san_pham/put_san_pham.yaml')
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

    @swag_from('../docs/swaggers/san_pham/delete_san_pham.yaml')
    @app.route('/api/san-pham/<int:id>', methods=['DELETE'])
    def delete_sp(id):
        # id = data.get('id')
        print('id:', id)
        # data = request.get_json()
        # id_ct = data.get('id_ct')
        # id_pl = data.get('id_pl')

        # if id_ct or id_pl:
        #     result = delete_chi_tiet_san_pham(id_ct=id_ct, id_pl=id_pl)
        # elif id:
        result = delete_san_pham(id=id)
        return result

class ChiTietSanPhamController(Resource):
    # @swag_from('')
    def get(self):
        data = request.args
        san_pham_id = data.get('san_pham_id')

        result = get_chi_tiet_san_pham_by_san_pham(san_pham_id)

        return result
    
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
