from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.GiamGiaService import *

class GiamGiaController(Resource):
    # @swag_from('')
    def get(self):
        data = request.args
        kw = data.get('kw')
        value = data.get('value')

        result = get_giam_gia(kw=kw, value=value)

        return result
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        value = data.get('value')

        result = post_giam_gia(name=name,value=value)

        return result

    def put(self):
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        value = data.get('value')

        result = put_giam_gia(id=id, name=name, value = value)

        return result

    def delete(self):
        data = request.get_json()
        id = data.get('id')

        result = delete_giam_gia(id=id)
        return result
