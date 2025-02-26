from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.BaoHanhService import *

class BaoHanhController(Resource):
    @swag_from('../docs/swaggers/bao_hanh/get_bao_hanh.yaml')
    def get(self):
        data = request.get_json()
        filter = data.get('filters')

        result = get_bao_hanh(filter=filter)

        return result
    
    @swag_from('../docs/swaggers/bao_hanh/post_bao_hanh.yaml')
    def post(self):
        data = request.get_json()
        ten = data.get('ten')

        result = post_bao_hanh(name=ten)

        return result

    @swag_from('../docs/swaggers/bao_hanh/put_bao_hanh.yaml')
    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')

        result = put_bao_hanh(id=id, name=name)

        return result

    @swag_from('../docs/swaggers/bao_hanh/put_bao_hanh.yaml')
    def delete(self):
        data = request.get_json()
        id = data.get('id')
        bao_hanh = BaoHanh.query.get(id)
        if bao_hanh is None:
            return get_error_response(ERROR_CODES.BAO_HANH_NOT_FOUND)
    
        result = delete_bao_hanh(id=id)
        return result