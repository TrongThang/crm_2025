from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.KhoService import *
from crm_app import app
from flasgger import swag_from 

class KhoController (Resource):
    @swag_from('../docs/swaggers/kho/get.yaml')
    def get(self):
        data     = request.args

        filter   = data.get("filters")
        limit    = data.get("limit")
        page     = data.get("page")
        order    = data.get("order")
        sort     = data.get("sort")

        result   = get_kho(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result

    @swag_from('../docs/swaggers/kho/post.yaml')
    def post(self):
        data    = request.get_json()
        ten     = data.get('ten')
        dia_chi = data.get('dia_chi')

        result  = post_kho(name=ten, address=dia_chi)
        return result

    @swag_from('../docs/swaggers/kho/put.yaml')
    def put(self):
        data    = request.get_json()
        id      = data.get('id')
        ten     = data.get('ten')
        dia_chi = data.get('dia_chi')

        result  = put_kho(id=id, name=ten, address=dia_chi)
        return result

    @swag_from('../docs/swaggers/kho/delete.yaml')
    @app.route('/api/kho/<int:id>', methods=['DELETE'])
    def delete_kho(id):
        try:
            print(id)
            result = delete_kho(id=id)
            
            return result
        except Exception as e:
            print("Lỗi:", e)
            return make_response(str(e), 500)
        
class TonKhoController(Resource):
    @swag_from('../docs/swaggers/kho/get_ton_kho.yaml')
    def get(seft):
        data     = request.args

        ctsp_id  = data.get("ctsp_id")
        result   = get_ton_kho(ctsp_id=ctsp_id)

        return result