from flask import request, jsonify, make_response
from crm_app import app
import jwt
from crm_app.helpers.redis import (
    get_role_by_employee,
    get_permission_by_role,
)

from crm_app.docs.containts import (
    get_error_response,
    ERROR_CODES
)

EXCLUDED_ROUTES = ["dang-nhap", "dang-ky"]
@app.before_request
def check_permission():
    try:
        if request.method == "OPTIONS":
            return
        
        pathname = request.path.rstrip('/').split('/')[1:]
        
        method = request.method
        pathname_first = pathname[0]
        if pathname_first == "apidocs"or pathname_first == "flasgger_static" or pathname_first == "apispec_1.json":
            return
        
        pathname = pathname[1:]
        if pathname[0] in EXCLUDED_ROUTES:
            return  # Bỏ qua middleware cho route đăng nhập, đăng ký
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Unauthorized"}), 401
        """
            Lấy action của người dùng {
                Kiểm tra: 
                    - Nếu như chỉ có pathname chỉ có 1 hành động thì kiểm tra thêm phương thức
                        + GET -> view-{pathname[0]]}
                        + POST -> create-{pathname[0]]}
                        + PUT -> update-{pathname[0]]}
                        + DELETE -> delete-{pathname[0]]}
                    - Nếu như có 2 hành động -> f"{pathname[1]}-{pathname[0]}"
                        + PATCH -> 
                        + Sau đó kiểm tra xem action này có nằm trong list quyền của nhân viên đó hay không
            }

            Lấy nhan_vien_id từ token -> vào redis, lấy quyền và chức vụ
            
        """
        action = ''
        pathname = pathname[1:]
        
        # quyen-han modify
        if len(pathname) > 1:
            for i in range(len(pathname) -1, -1, -1):
                action += pathname[i]
                if i > 0:
                    action += '-'

        if method == "GET":
            action = "view-" + action
        elif method == "POST":
            action = "create-" + action
        elif method == "PUT":
            action = "update-" + action
        elif method == "DELETE":
            action = "delete-" + action

        try:
            decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            request.user = decoded  # Lưu thông tin user vào request
            
            chuc_vu_id = get_role_by_employee(nhan_vien_id=decoded.get("nhan_vien_id"))
            if chuc_vu_id:
                chuc_vu_id = chuc_vu_id.decode("utf-8")
                
                if chuc_vu_id == '1':
                    return
                
                permission_list = get_permission_by_role(chuc_vu_id=chuc_vu_id)
                print("permission_list:",permission_list)
                if action in permission_list:
                    return 
                else:
                    return make_response(get_error_response(ERROR_CODES.POWERLESS), 403) 
                
            return make_response(get_error_response(ERROR_CODES.CHUC_VU_NOT_FOUND), 402) 

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token đã hết hạn!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token không hợp lệ!"}), 401
    except Exception as e:
        return make_response(str(e), 405)
        