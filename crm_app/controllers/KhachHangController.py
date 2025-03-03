from flask import request, jsonify
from flask_restful import Resource
from crm_app.services.KhachHangService import *

class KhachHangController (Resource):
    def get(self):
        data = request.args
        print("data:", data)
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        sort = data.get('sort')
        order = data.get('order')
        
        result = get_khach_hang(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result

    def post(self):
        data = request.get_json()
        ho_ten = data.get('ho_ten')
        dien_thoai = data.get('dien_thoai')
        dia_chi = data.get('dia_chi')

        result = post_khach_hang(name=ho_ten, address=dia_chi, phone=dien_thoai)

        return result
    
    def put(self):
        data = request.get_json()
        id = data.get('id')
        ho_ten = data.get('ho_ten')
        dien_thoai = data.get('dien_thoai')
        dia_chi = data.get('dia_chi')
        
        result = put_khach_hang(id=id, name=ho_ten, address=dia_chi, phone=dien_thoai)

        return result
    
    def delete(self):
        data = request.get_json()
        id = data.get('id')

        result = delete_khach_hang(id=id)
        return result