from flask import request, jsonify
from flask_restful import Resource

class NhanVienController (Resource):
    def get(self):
        data = request.args
        filter = data.get('filters')

        pass

    def post(self):
        data = request.form
        ho_ten = data.get('ho_ten')
        email = data.get('email')
        dien_thoai = data.get('dien_thoai')
        dia_chi = data.get('dia_chi')
        avatar = data.get('avatar')
        chuc_vu_id = data.get('chuc_vu_id')
        pass

    def put(self):
        data = request.form
        ho_ten = data.get('ho_ten')
        email = data.get('email')
        dien_thoai = data.get('dien_thoai')
        dia_chi = data.get('dia_chi')
        avatar = data.get('avatar')
        chuc_vu_id = data.get('chuc_vu_id')

        
        pass

    def delete(self):
        data = request.get_json()
        id = data.get('id')
        pass