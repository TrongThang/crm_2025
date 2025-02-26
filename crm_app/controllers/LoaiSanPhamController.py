from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.LoaiSanPhamService import *

class LoaiSanPhamController(Resource):
    # @swag_from('')
    def get(self):
        data = request.get_json()
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        result = get_loai_sp(filter=filter, limit=limit, page=page)

        return result
    
    def post(self):
        data = request.form
        name = data.get('ten')
        file = request.files.get('hinh_anh')
        result = post_loai_sp(name=name, file=file)

        return result

    def put(self):
        data = request.form
        id = data.get('id')
        name = data.get('ten')
        file = request.files.get('hinh_anh')

        result = put_loai_sp(id=id, name=name, file=file)

        return result

    def delete(self):
        data = request.get_json()
        id = data.get('id')

        result = delete_loai_sp(id=id)
        return result