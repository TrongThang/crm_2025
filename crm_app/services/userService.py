# from datetime import datetime, timedelta
import datetime
from flask import request, jsonify, make_response, g
from crm_app import app,db
from crm_app.models.NhanVien import NhanVien
from crm_app.docs.containts import ERROR_CODES, get_error_response
from crm_app.services.NhanVienService import get_nhan_vien_by_username
import bcrypt
import jwt
import hashlib
from crm_app import redis_client
from crm_app.helpers.redis import get_role_by_employee

REFRESH_SECRET_KEY = "IS@!(*RE(FRESH&*TOKEN))" 

def create_token(username, nhan_vien_id):
    token = jwt.encode(
        {
            'username': username,
            'nhan_vien_id': nhan_vien_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # Token hết hạn sau 30 giờQ
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return token

def create_refresh_token(username, nhan_vien_id):
    refresh_token = jwt.encode(
        {
            'username': username,
            'nhan_vien_id': nhan_vien_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Hết hạn sau 7 ngày
        },
        REFRESH_SECRET_KEY,
        algorithm='HS256'
    )
    return refresh_token

def getMe(token):
    if not token:
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        print('chuẩn bị lấy thông tin nhân viên')
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        print('decoded:', decoded)
        g.user = decoded
        chuc_vu_id = (get_role_by_employee(decoded.get("nhan_vien_id"))).decode('utf-8')
        print("chuc_vu_id:", chuc_vu_id)
        result = get_nhan_vien_by_username(username=decoded.get("username"), chuc_vu_id= chuc_vu_id)
        return result
            
    except jwt.ExpiredSignatureError:
        return make_response(jsonify({"message": "Token đã hết hạn!"}), 401)
    except jwt.InvalidTokenError:
        return make_response(jsonify({"message": "Token không hợp lệ!"}), 401)

def login(username, password):
    print('login', username, password)
    if password is None:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 401)

    user = NhanVien.query.filter_by(ten_dang_nhap=username, deleted_at=None).first()

    if not username or not user:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 401) 
    print(hashlib.md5(str(password).encode()).hexdigest() == user.mat_khau)
    if hashlib.md5(str(password).encode()).hexdigest() == user.mat_khau:
    # if bcrypt.checkpw(password.encode('utf-8'), user.mat_khau.encode('utf-8')):
        nhan_vien_id = user.id
        token = create_token(username=username, nhan_vien_id=nhan_vien_id)
        refresh_token = create_refresh_token(username=username, nhan_vien_id=nhan_vien_id)

        response_data = {"data" : {
            'refresh_token': refresh_token,
            # "access_token": token,
            'token': token, 
            'success': True
        }}

        return get_error_response(ERROR_CODES.SUCCESS, result=response_data)
    else:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 402)

def refresh_token():
    refresh_token = request.json.get("refresh_token")  # Nhận refresh token từ request
    if not refresh_token:
        return make_response(get_error_response(ERROR_CODES.TOKEN_INVALID), 401)

    try:
        # Giải mã Refresh Token
        decoded = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=['HS256'])

        # Tạo Access Token mới
        new_access_token = create_token(decoded["username"], decoded["nhan_vien_id"])
        
        return jsonify({
            "access_token": new_access_token,
            "success": True
        })
    except jwt.ExpiredSignatureError:
        return make_response(get_error_response(ERROR_CODES.TOKEN_EXPIRED), 403)
    except jwt.InvalidTokenError:
        return make_response(get_error_response(ERROR_CODES.TOKEN_INVALID), 403)

def change_password(username, password):
    if password is None:
        return make_response(jsonify({'message': 'Mật khẩu là bắt buộc', 'success': False}), 401)
    if username is None or username == '':
        return make_response(jsonify({'message':'Tên tài khoản là bắt buộc', 'success': False}), 401)
    
    nhan_vien = NhanVien.query.get(username)
    if nhan_vien:
        return make_response(jsonify({'message': 'Tên tài khoản đã tồn tại!', 'success': False}), 401)
    else:
        salt = bcrypt.gensalt()  # Tạo salt (tự động chọn độ mạnh)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        nhan_vien.password = password_hash.decode('utf-8')
        
        db.session.commit()

        return get_error_response(ERROR_CODES.SUCCESS)

def logout():
    data = request.json
    token = data.get("token")

    redis_client.delete(f"auth:{token}")
    return jsonify({"message": "Logged out"})