from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.ChucVuService import get_chuc_vu

class ChucVuController(Resource):
    def get(self):

        result = get_chuc_vu()

        return result
    
    def post(self):
        data = request.get_json()
        chuc_vu_id = data.get('chuc_vu_id')
        list_quyen = data.get('quyen')
        print(list_quyen)
        result = modify_quyen_chuc_vu(chuc_vu_id=chuc_vu_id, list_quyen=list_quyen)

        return result
    