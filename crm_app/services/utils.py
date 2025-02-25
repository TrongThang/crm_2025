from flask import jsonify, current_app
from crm_app.docs.containts import ERROR_CODES, MESSAGES, get_error_response
import os
import datetime

def serialize_data(data):
    def serialize_value(value):
        if isinstance(value, datetime.datetime):
            return value.isoformat()  # Chuyển datetime thành chuỗi ISO 8601
        elif isinstance(value, bytes):
            return value.decode('utf-8', errors='ignore')  # Chuyển bytes thành chuỗi UTF-8
        return value  # Giữ nguyên các kiểu dữ liệu khác

    return [
        {key: serialize_value(value) for key, value in dict(row).items()}
        for row in data
    ]

def validate_name(name, model,existing_id = None,max_length = 255):
    if name is None:
        return get_error_response(ERROR_CODES.DVT_NAME_REQUIRED)
    if len(name) > max_length:
        return get_error_response(ERROR_CODES.DVT_NAME_LENGTH)
    
    if isinstance(model, type) and hasattr(model, 'query'):
        existing_record = model.query.filter_by(ten=name).first()
        if existing_record and (existing_id is None or existing_record.id != existing_id):
            return get_error_response(ERROR_CODES.DVT_NAME_EXISTED)

        
    elif isinstance(model, (list, set)):
        if name in model:
            return get_error_response(ERROR_CODES.DVT_NAME_EXISTED)

        
    return None

def validate_number(number, model):
    if number is None:
        print('is None')
        return get_error_response(ERROR_CODES.PRICE_INVALID)

    try:
        number = float(number)
    except ValueError:
        print('is not Number')
        return get_error_response(ERROR_CODES.PRICE_INVALID) 
    
    if number <= 0:
        return get_error_response(ERROR_CODES.PRICE_LESSER_ZERO) 
    
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
        if filename:
            result = delete_file(upload_folder=upload_folder, filename=filename)
            # new_filename = filename
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
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
        if existing_record is None:
            return get_error_response(ERROR_CODES.NOT_FOUND)
        
    return True