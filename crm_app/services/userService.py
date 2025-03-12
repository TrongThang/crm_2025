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

def getMe(token):
    print("token:", token)
    if not token:
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        print('token:', token)
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        print('decoded:', decoded)
        g.user = decoded
        
        result = get_nhan_vien_by_username(decoded.get("username"))
        return get_error_response(ERROR_CODES.SUCCESS, result= result)
            
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token đã hết hạn!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token không hợp lệ!"}), 403

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
        print(123123)
        token = create_token(username=username, nhan_vien_id=nhan_vien_id)
        print(8695)
        return jsonify({'token': token, 'success': True})
    else:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 402)

def register(username, password):
    if password is None:
        return jsonify({'message':'Mật khẩu là bắt buộc', 'success': False})
    if username is None or username == '':
        return jsonify({'message':'Tên tài khoản là bắt buộc', 'success': False})
    
    user = NhanVien.query.get(username)
    if user:
        return jsonify({'message':'Tên tài khoản đã tồn tại!', 'success':False})
    else:
        salt = bcrypt.gensalt()  # Tạo salt (tự động chọn độ mạnh)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        newUser = NhanVien(username=username, password=password_hash.decode('utf-8'))
        db.session.add(newUser)
        db.session.commit()

        return jsonify({'message':'Tạo tài khoản thành công!', 'success':True})

def logout():
    data = request.json
    token = data.get("token")

    redis_client.delete(f"auth:{token}")
    return jsonify({"message": "Logged out"})