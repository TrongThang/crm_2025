from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.LoaiSanPhamService import *
from crm_app import app
class LoaiSanPhamController(Resource):
    @swag_from('../docs/swaggers/loai_san_pham/get_loai_san_pham.yaml')
    def get(self):
        data = request.args
        filter = data.getlist('filters')

        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')
        result = get_loai_sp(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result
    
    @swag_from('../docs/swaggers/loai_san_pham/post_loai_san_pham.yaml')
    def post(self):
        data = request.get_json()
        name = data.get('ten')
        file = data.get('hinh_anh')
        result = post_loai_sp(name=name, file=file)

        return result

    @swag_from('../docs/swaggers/loai_san_pham/put_loai_san_pham.yaml')
    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('ten')
        file = data.get('hinh_anh')
        print(id, name, file)
        result = put_loai_sp(id=id, name=name, file=file)

        return result

    @swag_from('../docs/swaggers/loai_san_pham/delete_loai_san_pham.yaml')
    @app.route('/api/loai-san-pham/<int:id>', methods=['DELETE'])
    def delete_loai_sp(id):
        result = delete_loai_sp(id=id)
        return result