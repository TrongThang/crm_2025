from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.LoaiSanPhamService import *

class LoaiSanPhamController(Resource):
    # @swag_from('')
    def get(self):
        data = request.args
        filter = data.get('filter')

        result = get_loai_sp(filter=filter)

        return result
    
    def post(self):
        data = request.form
        name = data.get('name')
        file = request.files.get('file')
        result = post_loai_sp(name=name, file=file)

        return result

    def put(self):
        data = request.form
        id = data.get('id')
        name = data.get('name')
        file = request.files.get('file')

        result = put_loai_sp(id=id, name=name, file=file)

        return result

    def delete(self):
        data = request.get_json()
        id = data.get('id')

        result = delete_loai_sp(id=id)
        return result

