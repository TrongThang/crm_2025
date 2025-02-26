from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.DonViTinhService import *

class DonViTinhController(Resource):
    # @swag_from('')
    def get(self):
        data = request.args
        filter = data.get('filters')

        result = get_don_vi_tinh(filter=filter)

        return result
    
    def post(self):
        data = request.get_json()
        name = data.get('name')

        result = post_don_vi_tinh(name=name)

        return result

    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')

        result = put_don_vi_tinh(id=id, name=name)

        return result

    def delete(self):
        data = request.get_json()
        id = data.get('id')

        result = delete_don_vi_tinh(id=id)
        return result

# def register_routes(api):
#     api.add_resource(DonViTinhController, '/api/don-vi-tinh')