from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.DonViTinhService import *
from crm_app import app

class DonViTinhController(Resource):
    @swag_from('../docs/swaggers/don_vi_tinh/get_don_vi_tinh.yaml')
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')

        print("filter:", filter)
        result = get_don_vi_tinh(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result
    
    @swag_from('../docs/swaggers/don_vi_tinh/post_don_vi_tinh.yaml')
    def post(self):
        data = request.get_json()
        ten = data.get('ten')

        result = post_don_vi_tinh(ten=ten)

        return result

    @swag_from('../docs/swaggers/don_vi_tinh/put_don_vi_tinh.yaml')
    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('ten')

        result = put_don_vi_tinh(id=id, name=name)

        return result

    @swag_from('../docs/swaggers/don_vi_tinh/delete_don_vi_tinh.yaml')
    @app.route('/api/don-vi-tinh/<int:id>', methods=['DELETE'])
    def delete(id):
        # data = request.path
        # id = data.get('id')

        result = delete_don_vi_tinh(id=id)
        return result

# def register_routes(api):
#     api.add_resource(DonViTinhController, '/api/don-vi-tinh')