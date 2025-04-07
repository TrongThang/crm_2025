from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.QuyenChucVuService import *
from flasgger import swag_from
from crm_app import app

class QuyenChucVuController(Resource):
    @swag_from('../docs/swaggers/quyen_han/get.yaml')
    @app.route('/api/quyen/<int:chuc_vu_id>', methods=['GET'])
    def get_quyen_han(chuc_vu_id):

        result = get_quyen_chuc_vu(chuc_vu_id=chuc_vu_id)

        return result
    
    @swag_from('../docs/swaggers/quyen_han/patch.yaml')
    @app.route('/api/quyen/modify', methods=["PATCH"])
    def patch_modify_permission():
        data = request.get_json()
        chuc_vu_id = data.get('chuc_vu_id')
        list_quyen = data.get('quyen')
        print(list_quyen)
        result = modify_quyen_chuc_vu(chuc_vu_id=chuc_vu_id, list_quyen=list_quyen)

        return result