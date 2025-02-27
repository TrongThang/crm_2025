from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.QuyenChucVuService import *

class QuyenChucVuController(Resource):
    def get(self):
        data = request.args
        chuc_vu_id = data.get('chuc_vu_id')

        result = get_quyen_chuc_vu(chuc_vu_id=chuc_vu_id)

        return result
    
    def post(self):
        data = request.args
        chuc_vu_id = data.get('chuc_vu_id')
        lst_quyen = data.getlist('lst_quyen')

        result = post_quyen_chuc_vu(chuc_vu_id=chuc_vu_id, lst_quyen=lst_quyen)

        return result
    