from flask import jsonify, current_app, make_response
from crm_app.docs.containts import ERROR_CODES, MESSAGES, get_error_response
import os
from datetime import datetime
import re


def validate_name(name, model,existing_id = None,max_length = 255, is_unique = True):
    if name is None:
        return make_response(get_error_response(ERROR_CODES.NAME_REQUIRED), 401)
    if len(name) > max_length:
        return make_response(get_error_response(ERROR_CODES.NAME_LENGTH), 401)
    
    if isinstance(model, type) and hasattr(model, 'query'):
        filter_field = 'ten' if hasattr(model, 'ten') else 'ten_san_pham' if hasattr(model, 'ten_san_pham') else None

        if filter_field and is_unique == True:
            existing_record = model.query.filter_by(ten=name).first()
            if existing_record and (existing_id is None or existing_record.id != existing_id):
                return make_response(get_error_response(ERROR_CODES.NAME_EXISTED), 401)

    elif isinstance(model, (list, set)):
        if name in model:
            return make_response(get_error_response(ERROR_CODES.NAME_EXISTED), 401)

        
    return None

def validate_number(number, model):
    if number is None:
        print('is None')
        return get_error_response(ERROR_CODES.NUMBER_INVALID)

    try:
        number = float(number)
    except ValueError:
        print('is not Number')
        return get_error_response(ERROR_CODES.PRICE_INVALID) 
    
    if number <= 0:
        return get_error_response(ERROR_CODES.PRICE_LESSER_ZERO) 
    
    return None

def validate_email(email):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    print('valid:', valid)
    if valid:
        return None
    
    return get_error_response(ERROR_CODES.EMAIL_INVALID)

def validate_phone(phone):
    rule = re.compile(r'^(03|05|07|08|09|01[2|6|8|9])\d{8}$')

    if not rule.search(phone):
        return get_error_response(ERROR_CODES.PHONE_INVALID)
    
    return None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder, filename = None, prefix="", suffix=""):
    print('file:', file)

    if not file or file.filename == '':
        return  { 
            "errorCode":ERROR_CODES.FILE_NOT_FOUND,
            "message":MESSAGES.FILE_NOT_FOUND
        }
    print('file:', file)
    if allowed_file(file.filename):
        # 📌 Lấy phần mở rộng file
        ext = file.filename.rsplit('.', 1)[1].lower()

        # 📌 Tạo thư mục lưu file riêng cho từng đối tượng nếu chưa có
        full_upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_folder)
        if not os.path.exists(full_upload_path):
            os.makedirs(full_upload_path, exist_ok=True)

        # 📌 Đổi tên file theo format YYYYMMDD_HHMMSS + tiền tố/hậu tố
        # if filename:
        #     # result = delete_file(upload_folder=upload_folder, filename=filename)
        #     new_filename = filename
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{prefix}{timestamp}{suffix}.{ext}"

        file_path = os.path.join(full_upload_path, new_filename)
        file.save(file_path)
        print('lưu hình ảnh loại sản phẩm')
        return {
            "errorCode":ERROR_CODES.SUCCESS,
            "message":MESSAGES.SUCCESS,
            "file_path": file_path,
            "filename": new_filename
        }

    return { "errorCode":ERROR_CODES.FILE_EXTENSION,
            "message":MESSAGES.FILE_EXTENSION}

def delete_file(upload_folder, filename):

    if not filename:
        return {"errorCode": ERROR_CODES.NOT_FOUND}, 404

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": MESSAGES.SUCCESS}, 200
    return {"errorCode": ERROR_CODES.NOT_FOUND}, 404

def isExistId(id, model):
    if isinstance(model, type) and hasattr(model, 'query'):
        existing_record = model.query.get(id)
        if existing_record:
            return True
        
    return False

def validate_datetime(datetime_check):
    # datetime.strptime(datetime_check, format)
    if isinstance(datetime_check, datetime):
        return True
    return False

def create_sku(upc, ct_san_pham_id, date_str, counter):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    formatted_date = date_obj.strftime("%m%d%Y")

    sku = f"{upc}-{ct_san_pham_id}-{formatted_date}-{counter:03}"

    return sku