from enum import Enum
from flask import jsonify
class ERROR_CODES(Enum):
    SUCCESS = 0
    NOT_FOUND = 404
    SERVER_EROR = 500
    BAD_REQUEST = 400

    FILE_SIZE = 1
    FILE_EXTENSION = 2
    FILE_NOT_FOUND = 3
    PRICE_INVALID = 4
    PRICE_GREATER_ZERO = 5
    PRICE_LESSER_ZERO = 6
    COST_PRICE_GREATER_SELL_PRICE = 7
    PHONE_INVALID = 8
    EMAIL_INVALID = 9
    NAME_EXISTED = 10
    NUMBER_INVALID = 11
    NAME_REQUIRED = 12 
    NAME_LENGTH = 13
    DATETIME_INVALID = 14
    PREPAID_INVALID = 15
    QUANTITY_NOT_ENOUGH = 16
    NOT_NUMBER = 17

    #SAN_PHAM - 1xxx
    SAN_PHAM_NOT_FOUND = 1001
    SAN_PHAM_NAME_REQUIRED = 1002
    SAN_PHAM_NAME_LENGTH = 1003
    SAN_PHAM_NAME_EXISTED = 1004
    SAN_PHAM_INVALID_ID = 1005

    #LOAI_SAN_PHAM - 2xxx
    LOAI_SP_NOT_FOUND = 2001
    LOAI_SP_NAME_REQUIRED = 2002
    LOAI_SP_NAME_LENGTH = 2003
    LOAI_SP_NAME_EXISTED = 2004
    LOAI_SP_INVALID_ID = 2005
    
    #DON_VI_TINH - 3xxx
    DVT_NOT_FOUND = 3001
    DVT_NAME_REQUIRED = 3002
    DVT_NAME_LENGTH = 3003
    DVT_NAME_EXISTED = 3004
    DVT_INVALID_ID = 3005

    #CHI TIET SAN PHAM - 4xxx
    CTSP_NOT_FOUND = 4001
    CTSP_NAME_REQUIRED  = 4002
    CTSP_NAME_LENGTH = 4003
    CTSP_NAME_EXISTED = 4004
    CTSP_INVALID_ID = 4005

    #BAO_HANH - 5xxx
    BAO_HANH_NOT_FOUND = 5001
    BAO_HANH_NAME_REQUIRED = 5002
    BAO_HANH_NAME_LENGTH = 5003
    BAO_HANH_NAME_EXISTED = 5004
    BAO_HANH_INVALID_ID = 5005

    #GIAM_GIA - 6xxx
    GIAM_GIA_NOT_FOUND = 6001
    GIAM_GIA_NAME_REQUIRED = 6002
    GIAM_GIA_NAME_LENGTH = 6003
    GIAM_GIA_NAME_EXISTED = 6004
    GIAM_GIA_INVALID_ID = 6005
    GIAM_GIA_INVALID_PERCENT = 6006

    #NHAN_VIEN - 7xxx
    ACCOUNT_INVALID = 7001
    USERNAME_LENGTH = 7002
    PASSWORD_LENGTH = 7003
    NHAN_VIEN_NAME_REQUIRED = 7004
    NHAN_VIEN_NOT_FOUND = 7005
    NHAN_VIEN_NAME_LENGTH = 7006

    #NHA_PHAN_PHOI - 8xxx
    NHA_PHAN_PHOI_NOT_FOUND = 8001
    NHA_PHAN_PHOI_NAME_LRNGTH = 8002

    #KHO - 9xxx
    KHO_NOT_FOUND = 9001


class MESSAGES(Enum):
    SUCCESS = "Thành công"
    NOT_FOUND = "Không tìm thấy dữ liệu"
    SERVER_ERROR = "Lỗi máy chủ nội bộ"
    BAD_REQUEST = "Yêu cầu không hợp lệ"

    FILE_SIZE = "Kích thước ảnh vượt quá giới hạn cho phép"
    FILE_EXTENSION = "Định dạng ảnh không hợp lệ"
    FILE_NOT_FOUND = "Không có file được gửi"
    PRICE_INVALID = "Giá sản phẩm không hợp lệ!"
    # PRICE_GREATER_ZERO = "Giá phải lớn hơn 0"
    PRICE_LESSER_ZERO = "Giá sản phẩm phải lớn hơn 0"
    COST_PRICE_GREATER_SELL_PRICE = "Giá nhập phải nhỏ hơn giá bán"
    PHONE_INVALID = "Số điện thoại không hợp lệ!"
    EMAIL_INVALID = "Email không hợp lệ!"
    NAME_EXISTED = "Tên đã tồn tại!"
    NUMBER_INVALID = "Số không hợp lệ!"
    NAME_REQUIRED = "Yêu cầu nhập tên!"
    DATETIME_INVALID = "Ngày giờ không hợp lệ!"
    PREPAID_INVALID = "Giá trị trả trước không hợp lệ!"
    QUANTITY_NOT_ENOUGH = "Số lượng sản phẩm trong lô hàng không đủ đáp ứng"
    NOT_NUMBER = "Không phải số"

    # SAN_PHAM - 1xxx
    SAN_PHAM_NOT_FOUND = "Không tìm thấy sản phẩm"
    SAN_PHAM_NAME_REQUIRED = "Tên sản phẩm là bắt buộc"
    SAN_PHAM_NAME_LENGTH = "Tên sản phẩm quá dài"
    SAN_PHAM_NAME_EXISTED = "Tên sản phẩm đã tồn tại"
    SAN_PHAM_INVALID_ID = "ID sản phẩm không hợp lệ"

    # LOAI_SAN_PHAM - 2xxx
    LOAI_SP_NOT_FOUND = "Không tìm thấy loại sản phẩm"
    LOAI_SP_NAME_REQUIRED = "Tên loại sản phẩm là bắt buộc"
    LOAI_SP_NAME_LENGTH = "Tên loại sản phẩm quá dài"
    LOAI_SP_NAME_EXISTED = "Tên loại sản phẩm đã tồn tại"
    LOAI_SP_INVALID_ID = "ID loại sản phẩm không hợp lệ"

    # DON_VI_TINH - 3xxx
    DVT_NOT_FOUND = "Không tìm thấy đơn vị tính"
    DVT_NAME_REQUIRED = "Tên đơn vị tính là bắt buộc"
    DVT_NAME_LENGTH = "Tên đơn vị tính quá dài"
    DVT_NAME_EXISTED = "Tên đơn vị tính đã tồn tại"
    DVT_INVALID_ID = "ID đơn vị tính không hợp lệ"

    # CHI_TIET_SAN_PHAM - 4xxx
    CTSP_NOT_FOUND = "Không tìm thấy chi tiết sản phẩm"
    CTSP_NAME_REQUIRED = "Tên chi tiết sản phẩm là bắt buộc"
    CTSP_NAME_LENGTH = "Tên chi tiết sản phẩm quá dài"
    CTSP_NAME_EXISTED = "Tên chi tiết sản phẩm đã tồn tại"
    CTSP_INVALID_ID = "ID chi tiết sản phẩm không hợp lệ"
    CTSP_PRICE_GRETER_ZERO = "Giá sản phẩm phải lớn hơn 0"
    CTSP_PRICE_LESSER_ZERO = "Giá sản phẩm không thể nhỏ hơn 0"

    # BAO_HANH - 5xxx
    BAO_HANH_NOT_FOUND = "Không tìm thấy thông tin bảo hành"
    BAO_HANH_NAME_REQUIRED = "Tên bảo hành là bắt buộc"
    BAO_HANH_NAME_LENGTH = "Tên bảo hành quá dài"
    BAO_HANH_NAME_EXISTED = "Tên bảo hành đã tồn tại"
    BAO_HANH_INVALID_ID = "ID bảo hành không hợp lệ"

    # GIAM_GIA - 6xxx
    GIAM_GIA_NOT_FOUND = "Không tìm thấy thông tin giảm giá"
    GIAM_GIA_NAME_REQUIRED = "Tên giảm giá là bắt buộc"
    GIAM_GIA_NAME_LENGTH = "Tên giảm giá quá dài"
    GIAM_GIA_NAME_EXISTED = "Tên giảm giá đã tồn tại"
    GIAM_GIA_INVALID_ID = "ID giảm giá không hợp lệ"
    GIAM_GIA_INVALID_PERCENT = "Mức giá giảm không được lớn hơn 90%"

    # NHAN_VIEN - 7xxx
    ACCOUNT_INVALID = "Tài khoản không hợp lệ"
    USERNAME_LENGTH = "Tên đăng nhập quá dài hoặc quá ngắn"
    PASSWORD_LENGTH = "Mật khẩu quá dài hoặc quá ngắn"
    NHAN_VIEN_NAME_LENGTH = "Họ tên từ 1 đến 255 ký tự"

    #CHUC_VU - 8xxx
    CHUC_VU_NOT_FOUND = "Kh"
    CHUC_VU_NAME_LENGTH = ""
    CHUC_VU_NAME_REQUIRED = ""

    NHA_PHAN_PHOI_NOT_FOUND = "Không tìm thấy nhà phân phối hợp lệ"
    NHA_PHAN_PHOI_NAME_LENGTH = "Tên nhà phân phối từ 1 đến 255 ký tự"

    KHO_NOT_FOUND = "Không tìm thấy kho hợp lệ"

    
def get_error_response(error_code: ERROR_CODES, result = None):
    """Trả về response JSON chứa errorCode và message tương ứng"""
    message = MESSAGES[error_code.name].value if error_code.name in MESSAGES.__members__ else "Lỗi không xác định"

    return jsonify({
        "error": error_code.value,
        "message": message,
        "data": result
    })