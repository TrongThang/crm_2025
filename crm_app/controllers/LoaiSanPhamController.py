from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.LoaiSanPhamService import *

class LoaiSanPhamController(Resource):
    @swag_from('../docs/swaggers/loai_san_pham/get_loai_san_pham.yaml')
    def get(self):
        data = request.args
        filter = data.getlist('filters')
        print("filter:", filter)
        filters = []
        index = 0
        while f'filters[{index}][field]' in data:
            filters.append({
                'field': data.get(f'filters[{index}][field]'),
                'condition': data.get(f'filters[{index}][condition]'),
                'value': data.get(f'filters[{index}][value]', '')
            })
            index += 1
        print("filter:", filters)

        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')
        result = get_loai_sp(filter=filters, limit=limit, page=page, sort=sort, order=order)

        return result
    
    @swag_from('../docs/swaggers/loai_san_pham/post_loai_san_pham.yaml')
    def post(self):
        data = request.form
        name = data.get('ten')
        file = request.files.get('hinh_anh')
        result = post_loai_sp(name=name, file=file)

        return result

    @swag_from('../docs/swaggers/loai_san_pham/put_loai_san_pham.yaml')
    def put(self):
        data = request.form
        id = data.get('id')
        name = data.get('ten')
        file = request.files.get('hinh_anh')
        print(id, name, file)
        result = put_loai_sp(id=id, name=name, file=file)

        return result

    @swag_from('../docs/swaggers/loai_san_pham/delete_loai_san_pham.yaml')
    def delete(self):
        # data = request.get_json()
        data = request.args
        id = data.get('id')
        print("id:", id)
        result = delete_loai_sp(id=id)
        return result