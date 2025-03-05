# from datetime import datetime, timedelta
import datetime
from flask import request, jsonify, make_response
from crm_app import app,db
from functools import wraps
from crm_app.models.NhanVien import NhanVien
from crm_app.docs.containts import ERROR_CODES
from crm_app.services.utils import validate_name
import bcrypt
import jwt
import hashlib
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379)

def create_token(username):
    token = jwt.encode(
        {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token hết hạn sau 30 phút
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return token

def login(username, password):
    print('login', username, password)
    if password is None:
        return make_response(jsonify({'message': 'Tài khoản hoặc mật khẩu không chinnh xác', 'errorCode': 1}), 401)

    user = NhanVien.query.filter_by(ten_dang_nhap=username).first()

    print('users:', user)
    if not username or not user:
        return make_response(jsonify({'message': 'Không tìm thấy tên tài khoản người dùng', 'errorCode': 1}), 401)
    
    # error = validate_name(name=username, model=NhanVien, max_length=50)
    # if error:
    #     return error
    
    # error = validate_name(name=password, model=NhanVien, max_length=50)
    # if error:
    #     return error
    
    if hashlib.md5(password.encode()).hexdigest() == user.mat_khau:
    # if bcrypt.checkpw(password.encode('utf-8'), user.mat_khau.encode('utf-8')):
        token = create_token(username)
        redis_client.setex(f"auth:{token}", 3600, ",".join())
        return jsonify({'token': token, 'success': True})
    else:
        return make_response(jsonify({'message':'Mật khẩu không chính xác', 'errorCode': 1}), 401)

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
        newUser = User(username=username, password=password_hash.decode('utf-8'))
        db.session.add(newUser)
        db.session.commit()

        return jsonify({'message':'Tạo tài khoản thành công!', 'success':True})

def logout():
    data = request.json
    token = data.get("token")

    redis_client.delete(f"auth:{token}")
    return jsonify({"message": "Logged out"})