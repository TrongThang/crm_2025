from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.SanPhamService import *

class SanPhamController(Resource):
    # @swag_from('')
    def get(self):
        data = request.args
        ten = data.get('ten')
        mota = data.get('mota')
        vat = data.get('vat')
        lsp = data.get('lsp')
        dvt = data.get('dvt')
        gg = data.get('gg')
        bh = data.get('bh')

        result = get_san_pham(ten=ten, mota=mota, vat=vat, lsp=lsp, dvt=dvt, gg=gg, bh=bh)
        
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

        result = post_san_pham(ten=ten, upc=upc, vat=vat, mo_ta=mo_ta, trang_thai=trang_thai, file=file, loai_id=loai_id, dvt_id=dvt_id, gg_id=gg_id, bh_id=bh_id)

        return result 

    def put(self):
        pass

    def delete(self):
        pass

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
