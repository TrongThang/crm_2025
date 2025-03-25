from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.ChucVuService import *
from crm_app import app

class ChucVuController(Resource):
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')

        result = get_chuc_vu(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result
    
    def post(self):
        data = request.get_json()
        ten = data.get('ten')
        
        result = post_chuc_vu(ten=ten)

        return result
    
    def put(self):
        data = request.get_json()
        id = data.get('id')
        ten = data.get('ten')
        
        result = put_chuc_vu(id=id, ten=ten)

        return result
    
    @app.route('/api/chuc-vu/<int:id>', methods=['DELETE'])
    def delete_chuc_vu(id):
        
        result = delete_chuc_vu(id=id)

        return result
    