from flask import request, jsonify
from flasgger import swag_from
from flask_restful import Resource
from crm_app.services.NhaPhanPhoiService import *
from crm_app import app
class NhaPhanPhoiController (Resource):
    @swag_from('../docs/swaggers/nha_phan_phoi/get_nha_phan_phoi.yaml')
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        sort = data.get('sort')
        order = data.get('order')
        
        result = get_nha_phan_phoi(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result

    @swag_from('../docs/swaggers/nha_phan_phoi/post_nha_phan_phoi.yaml')
    def post(self):
        data = request.get_json()
        ten = data.get('ten')
        email = data.get('email')
        dien_thoai = data.get('dien_thoai')
        dia_chi = data.get('dia_chi')
        ds_san_pham = data.get('ds_san_pham')
        result = post_nha_phan_phoi(name=ten, address=dia_chi, phone=dien_thoai, email=email, ds_san_pham=ds_san_pham)

        return result
    
    @swag_from('../docs/swaggers/nha_phan_phoi/put_nha_phan_phoi.yaml')
    def put(self):
        data = request.get_json()
        id = data.get('id')
        ten = data.get('ten')
        email = data.get('email')
        dien_thoai = data.get('dien_thoai')
        dia_chi = data.get('dia_chi')
        ds_san_pham = data.get('ds_san_pham')
        result = put_nha_phan_phoi(id=id, name=ten, address=dia_chi, phone=dien_thoai, email=email, ds_san_pham=ds_san_pham)

        return result
    
    @swag_from('../docs/swaggers/nha_phan_phoi/delete_nha_phan_phoi.yaml')
    @app.route('/api/nha-phan-phoi/<int:id>', methods=['DELETE'])
    def delete_nha_phan_phoi(id):
        result = delete_nha_phan_phoi(id=id)
        return result