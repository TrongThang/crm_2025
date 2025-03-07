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
        data = request.get_json()
        hinh_anh = data.get('hinh_anh')
        ten = data.get('ten')
        upc = data.get('upc')
        vat = data.get('vat')
        mo_ta = data.get('mo_ta')
        trang_thai = data.get('trang_thai')
        loai_id = data.get('loai_san_pham_id')
        dvt_id = data.get('don_vi_tinh_id')
        gg_id = data.get('giam_gia_id')
        bh_id = data.get('bao_hanh_id')
        print("form:", request.form)
        chi_tiet_san_pham = data.get('chi_tiet_san_pham')

        result = post_san_pham(ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, hinh_anh=hinh_anh, loai_id=loai_id, dvt_id=dvt_id, gg_id=gg_id, bh_id=bh_id, chi_tiet_san_pham=chi_tiet_san_pham)
        return result 

    @swag_from('../docs/swaggers/san_pham/put_san_pham.yaml')
    def put(self):
        data = request.get_json()
        hinh_anh = data.get('hinh_anh')
        id = data.get('id')
        ten = data.get('ten')
        upc = data.get('upc')
        vat = data.get('vat')
        mo_ta = data.get('mo_ta')
        trang_thai = data.get('trang_thai')
        loai_id = data.get('loai_san_pham_id')
        dvt_id = data.get('don_vi_tinh_id')
        gg_id = data.get('giam_gia_id')
        bh_id = data.get('bao_hanh_id')
        
        chi_tiet_san_pham = data.get('chi_tiet_san_pham')

        result = put_san_pham(id=id, ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, hinh_anh=hinh_anh, loai_id=loai_id, dvt_id=dvt_id, gg_id=gg_id, bh_id=bh_id, chi_tiet_san_pham = chi_tiet_san_pham)

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
    @app.route('/api/chi-tiet-san-pham/<int:id>', methods=['GET'])
    def get(id):

        result = get_chi_tiet_san_pham_by_san_pham(san_pham_id=id)

        return result
    
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
