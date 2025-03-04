from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.BaoHanhService import *
from crm_app import app
class BaoHanhController(Resource):
    @swag_from('../docs/swaggers/bao_hanh/get_bao_hanh.yaml')
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')
        result = get_bao_hanh(filter=filter, limit=limit, page=page, sort=sort, order=order)

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
        name = data.get('ten')

        result = put_bao_hanh(id=id, name=name)

        return result

    @swag_from('../docs/swaggers/bao_hanh/delete_bao_hanh.yaml')
    @app.route('/api/thoi-gian-bao-hanh/<int:id>', methods=['DELETE'])
    def delete_bao_hanh(id):
        result = delete_bao_hanh(id=id)
        return result