from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.GiamGiaService import *
from crm_app import app
class GiamGiaController(Resource):
    @swag_from('../docs/swaggers/giam_gia/get_giam_gia.yaml')
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')

        result = get_giam_gia(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result
    
    @swag_from('../docs/swaggers/giam_gia/post_giam_gia.yaml')
    def post(self):
        data = request.get_json()
        ten = data.get('ten')
        value = data.get('gia_tri')
        result = post_giam_gia(ten=ten,value=value)

        return result

    @swag_from('../docs/swaggers/giam_gia/put_giam_gia.yaml')
    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('ten')
        value = data.get('gia_tri')

        result = put_giam_gia(id=id, name=name, value = value)

        return result

    # @swag_from('../docs/swaggers/giam_gia/delete_giam_gia.yaml')
    @app.route('/api/loai-giam-gia/<int:id>', methods=['DELETE'])
    def delete_giam_gia(id):
        # data = request.get_json()
        # id = data.get('id')
        print("id = ",id)
        result = delete_giam_gia(id=id)
        return result