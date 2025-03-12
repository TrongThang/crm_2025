from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.KhoService import *
from crm_app import app

class KhoController (Resource):
    def get(self):
        data     = request.args

        filter   = data.get("filters")
        limit    = data.get("limit")
        page     = data.get("page")
        order    = data.get("order")
        sort     = data.get("sort")

        result   = get_kho(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result

    def post(self):
        data    = request.get_json()
        ten     = data.get('ten')
        dia_chi = data.get('dia_chi')

        result  = post_kho(name=ten, address=dia_chi)
        return result

    def put(self):
        data    = request.get_json()
        id      = data.get('id')
        ten     = data.get('ten')
        dia_chi = data.get('dia_chi')

        result  = put_kho(id=id, name=ten, address=dia_chi)
        return result

    @app.route('/api/kho/<int:id>', methods=['DELETE'])
    def delete_kho(id):
        try:
            print(id)
            result = delete_kho(id=id)
            
            return result
        except Exception as e:
            print("Lỗi:", e)
            return make_response(str(e), 500)