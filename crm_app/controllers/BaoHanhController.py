from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.BaoHanhService import *

class BaoHanhController(Resource):
    # @swag_from('')
    def get(self):
        data = request.args
        filter = data.get('filter')

        result = get_bao_hanh(filter=filter)

        return result
    
    def post(self):
        data = request.get_json()
        name = data.get('name')

        result = post_bao_hanh(name=name)

        return result

    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')

        result = put_bao_hanh(id=id, name=name)

        return result

    def delete(self):
        data = request.get_json()
        id = data.get('id')
        bao_hanh = BaoHanh.query.get(id)
        if bao_hanh is None:
            return get_error_response(ERROR_CODES.BAO_HANH_NOT_FOUND)
    
        result = delete_bao_hanh(id=id)
        return result