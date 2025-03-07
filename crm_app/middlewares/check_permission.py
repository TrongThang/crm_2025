from flask import request, jsonify
from crm_app import app
import jwt

EXCLUDED_ROUTES = ["dang-nhap", "dang-ky"]
@app.before_request
def check_permission():
    last_segment = request.path.rstrip('/').split('/')[-1]

    method = request.method
    if last_segment in EXCLUDED_ROUTES and method == "POST":
        return  # Bỏ qua middleware cho route đăng nhập, đăng ký
    print('bắt đầu check quyền')
    token = request.headers.get("Authorization")
    if not token or token != "Bearer my_secret_token":
        return jsonify({"message": "Unauthorized"}), 403
    
    try:
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        request.user = decoded  # Lưu thông tin user vào request
        print(request.user)
        print("decoded:", decoded)
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token đã hết hạn!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token không hợp lệ!"}), 403