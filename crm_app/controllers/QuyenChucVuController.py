from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.QuyenChucVuService import *

class QuyenChucVuController(Resource):
    def get(self):
        data = request.args
        chuc_vu_id = data.get('chuc_vu_id')

        result = get_quyen_chuc_vu(chuc_vu_id=chuc_vu_id)

        return result
    