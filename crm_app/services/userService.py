# from datetime import datetime, timedelta
import datetime
from flask import request, jsonify, make_response
from crm_app import app,db
from crm_app.models.NhanVien import NhanVien
from crm_app.docs.containts import ERROR_CODES, get_error_response
import bcrypt
import jwt
import hashlib
from crm_app import redis_client

def create_token(username, chuc_vu_id):
    token = jwt.encode(
        {
            'username': username,
            'chuc_vu_id': chuc_vu_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token hết hạn sau 30 phút
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return token

def login(username, password):
    print('login', username, password)
    if password is None:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 401)

    user = NhanVien.query.filter_by(ten_dang_nhap=username, deleted_at=None).first()

    if not username or not user:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 401)

    if hashlib.md5(str(password).encode()).hexdigest() == user.mat_khau:
    # if bcrypt.checkpw(password.encode('utf-8'), user.mat_khau.encode('utf-8')):
        chuc_vu_id = user.chuc_vu_id
        
        token = create_token(username=username, chuc_vu_id=chuc_vu_id)
        
        return jsonify({'token': token, 'success': True})
    else:
        return make_response(get_error_response(ERROR_CODES.ACCOUNT_INVALID), 401)

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