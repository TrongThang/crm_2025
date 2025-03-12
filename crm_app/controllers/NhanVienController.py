from flask import request, jsonify
from flask_restful import Resource
from flasgger import swag_from
from crm_app.services.NhanVienService import *
from crm_app import app

class NhanVienController (Resource):
    @swag_from('../docs/swaggers/nhan_vien/get_detail_nhan_vien.yaml')
    @app.route('/api/nhan-vien/chi-tiet')
    def get_detail():
        data = request.args
        username = data.get('ten_dang_nhap')
        result   = get_nhan_vien_by_username(username)

        return result
    
    @swag_from('../docs/swaggers/nhan_vien/get_nhan_vien.yaml')
    def get(self):
        data = request.args
        filter = data.get('filters')
        limit = data.get('limit')
        page = data.get('page')
        order = data.get('order')
        sort = data.get('sort')
        
        result = get_nhan_vien(filter=filter, limit=limit, page=page, sort=sort, order=order)

        return result

    @swag_from('../docs/swaggers/nhan_vien/post_nhan_vien.yaml')
    def post(self):
        try:
            data = request.get_json()
            ho_ten = data.get('ho_ten')
            username = data.get('ten_dang_nhap')
            email = data.get('email')
            dien_thoai = data.get('dien_thoai')
            dia_chi = data.get('dia_chi')
            avatar = data.get('avatar')
            chuc_vu_id = data.get('chuc_vu_id')

            result = post_nhan_vien(ho_ten=ho_ten, username=username, email=email, dia_chi=dia_chi, dien_thoai=dien_thoai, avatar=avatar, chuc_vu_id=chuc_vu_id)
            return result
        except Exception as e:
            print("Lỗi:", e)
            return make_response(str(e), 500)

    # @swag_from('../docs/swaggers/nhan_vien/put_nhan_vien.yaml')
    def put(self):
        try:
            data = request.get_json()
            id = data.get('id')
            username = data.get('ten_dang_nhap')
            ho_ten = data.get('ho_ten')
            email = data.get('email')
            dien_thoai = data.get('dien_thoai')
            dia_chi = data.get('dia_chi')
            avatar = data.get('avatar')
            chuc_vu_id = data.get('chuc_vu_id')
            print('data:', data)
            result = put_nhan_vien(id=id, ho_ten=ho_ten, username=username, email=email, dia_chi=dia_chi, dien_thoai=dien_thoai, avatar=avatar, chuc_vu_id=chuc_vu_id)
            return result
        except Exception as e:
            print("Lỗi:", e)
            return make_response(str(e), 500)

    # @swag_from('../docs/swaggers/nhan_vien/delete_nhan_vien.yaml')
    @app.route('/api/nhan-vien/<int:id>', methods=['DELETE'])
    def delete_nv(id):
        try:
            print(id)
            result = delete_nhan_vien(id=id)
            
            return result
        except Exception as e:
            print("Lỗi:", e)
            return make_response(str(e), 500)