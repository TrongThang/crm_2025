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
    NO_PRODUCT_SELECTED = 18
    CHIET_KHAU_INVALID = 19
    SAN_PHAM_OF_NHA_PHAN_PHOI_EXISTED = 20
    VAT_INVALID = 21
    TOTAL_MONEY_INVALID = 22
    TOTAL_AMOUNT_INVALID = 23
    TOTAL_COST_INVALID = 24
    SO_LUONG_TRA_GREATED_THAN_ZERO = 25
    INVALID_COST = 26
    GIA_NHAP_INVALID = 27

    #SAN_PHAM - 1xxx
    SAN_PHAM_NOT_FOUND = 1001
    SAN_PHAM_NAME_REQUIRED = 1002
    SAN_PHAM_NAME_LENGTH = 1003
    SAN_PHAM_NAME_EXISTED = 1004
    SAN_PHAM_UPC_EXISTED = 1004
    SAN_PHAM_INVALID_ID = 1005
    SAN_PHAM_NOT_FOUND_TRANG_THAI = 1006

    SAN_PHAM_REFERENCE_NHA_PHAN_PHOI = 1008
    SAN_PHAM_REFERENCE_CTSP = 1007
    SAN_PHAM_REFERENCE_CHI_TIET_NHAP_HD = 1010
    SAN_PHAM_REFERENCE_CHI_TIET_XUAT_HD = 1009
    SAN_PHAM_REFERENCE_TON_KHO = 1011
    
    #LOAI_SAN_PHAM - 2xxx
    LOAI_SP_NOT_FOUND = 2001
    LOAI_SP_NAME_REQUIRED = 2002
    LOAI_SP_NAME_LENGTH = 2003
    LOAI_SP_NAME_EXISTED = 2004
    LOAI_SP_INVALID_ID = 2005
    SAN_PHAM_OF_LSP_EXITED = 2006
    
    #DON_VI_TINH - 3xxx
    DVT_NOT_FOUND = 3001
    DVT_NAME_REQUIRED = 3002
    DVT_NAME_LENGTH = 3003
    DVT_NAME_EXISTED = 3004
    DVT_INVALID_ID = 3005
    DVT_REFERENCE_SAN_PHAM = 3003


    #CHI TIET SAN PHAM - 4xxx
    CTSP_NOT_FOUND = 4001
    CTSP_NAME_REQUIRED  = 4002
    CTSP_NAME_LENGTH = 4003
    CTSP_NAME_EXISTED = 4004
    CTSP_INVALID_ID = 4005
    CTSP_REFERENCE_CHI_TIET_NHAP_HD = 4006
    CTSP_REFERENCE_CHI_TIET_XUAT_HD = 4007
    CTSP_REFERENCE_TON_KHO = 4008
    
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
    USERNAME_EXISTED = 7003
    PASSWORD_LENGTH = 7003
    NHAN_VIEN_NAME_REQUIRED = 7004
    NHAN_VIEN_NOT_FOUND = 7005
    NHAN_VIEN_NAME_LENGTH = 7006
    NHAN_VIEN_REFERENCE_HOA_DON_XUAT = 7007

    #NHA_PHAN_PHOI - 8xxx
    NHA_PHAN_PHOI_NOT_FOUND = 8001
    NHA_PHAN_PHOI_NAME_LRNGTH = 8002
    NHA_PHAN_PHOI_REFERENCE_SAN_PHAM = 8003
    NHA_PHAN_PHOI_REFERENCE_HOA_DON_NHAP = 8004

    #KHO - 9xxx
    KHO_NOT_FOUND = 9001
    KHO_REFERENCE_HOA_DON_NHAP = 9002
    KHO_REFERENCE_HOA_DON_XUAT = 9003
    KHO_NOT_EXISTED_SKU = 9004
    KHO_NOT_QUANTITY_FOR_RETURNS = 9005
    KHO_NOT_QUANTITY_FOR_SALE = 9006

    #HOA_DON_NHAP - 11xx
    HOA_DON_NHAP_NOT_FOUND = 1107
    HOA_DON_NHAP_PREPAID_LESS_ZERO = 1101
    HOA_DON_NHAP_PREPAID_GREATER_TOTAL_MONEY = 1102
    HOA_DON_NHAP_PREPAID_NOT_SAME = 1103
    HOA_DON_NHAP_TOTAL_MONEY_NOT_SAME = 1104
    
    HOA_DON_XUAT_TOTAL_MONEY_NOT_SAME = 1105
    INVALID_GIFT_FLAG =  1106

    HOA_DON_NHAP_SL_TRA_GREATED_THAN_SO_LUONG_SALE = 1107
    HOA_DON_XUAT_SO_LUONG_BAN_NOT_SAME = 1108
    DELIVERED_STATUS_INVALID = 1109
    LOCK_STATUS_INVALID = 1109
    HOA_DON_NHAP_IS_LOCK = 1110

    
    #CHUC_VU- 12xx
    CHUC_VU_NOT_FOUND = 1201
    CHUC_NANG_NOT_FOUND = 1201
    
    #HOA DON XUAT - 13xx
    HOA_DON_XUAT_NOT_FOUND = 1301
    HOA_DON_XUAT_NOT_STATUS = 1302

    #QUYEN HAN - 14xx
    POWERLESS = 1401

    #KHACH HANG - 15xx
    KHACH_HANG_NOT_FOUND = 1501
    KHACH_HANG_REFERENCE_HOA_DON_XUAT = 1502


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
    NO_PRODUCT_SELECTED = "Không có sản phẩm nào được chọn!"
    CHIET_KHAU_INVALID = "Chiết khấu phải từ 0 đến 99%"
    SAN_PHAM_OF_NHA_PHAN_PHOI_EXISTED = "Đã tồn tại sản phẩm này trong nhà phân phối!"
    TOTAL_MONEY_INVALID = "Tổng tiền không giống với thông tin khách hàng gửi về!"
    TOTAL_AMOUNT_INVALID = "Thành tiền không giống với thông tin khách hàng gửi về!"
    TOTAL_COST_INVALID = "Tổng giá nhập không giống với thông tin khách hàng gửi về!"
    SO_LUONG_TRA_GREATED_THAN_ZERO = "Số lượng trả của sản phẩm phải lớn hơn 0!"
    INVALID_COST = "Giá nhập không hợp lệ!"
    # SAN_PHAM - 1xxx
    SAN_PHAM_NOT_FOUND = "Không tìm thấy sản phẩm"
    SAN_PHAM_NAME_REQUIRED = "Tên sản phẩm là bắt buộc"
    SAN_PHAM_NAME_LENGTH = "Tên sản phẩm quá dài"
    SAN_PHAM_NAME_EXISTED = "Tên sản phẩm đã tồn tại"
    SAN_PHAM_INVALID_ID = "ID sản phẩm không hợp lệ"
    SAN_PHAM_UPC_EXISTED = "UPC của sản phẩm đã tồn tại!"
    SAN_PHAM_NOT_FOUND_TRANG_THAI = "Trạng thái của sản phẩm không tồn tại!"

    SAN_PHAM_REFERENCE_CTSP = "Sản phẩm này có tham chiếu đến chi tiết sản phẩm đang còn hoạt động!"
    SAN_PHAM_REFERENCE_NHA_PHAN_PHOI = "Sản phẩm này có tham chiếu đến nhà phân phối đang còn hoạt động!"
    SAN_PHAM_REFERENCE_CHI_TIET_XUAT_HD = "Sản phẩm này có tham chiếu đến hoá đơn xuất hàng!"
    SAN_PHAM_REFERENCE_CHI_TIET_NHAP_HD = "Sản phẩm này có tham chiếu đến hoá đơn nhập hàng!"
    SAN_PHAM_REFERENCE_TON_KHO = "Sản phẩm này vẫn còn trong kho và chưa bị xoá!"


    # LOAI_SAN_PHAM - 2xxx
    LOAI_SP_NOT_FOUND = "Không tìm thấy loại sản phẩm"
    LOAI_SP_NAME_REQUIRED = "Tên loại sản phẩm là bắt buộc"
    LOAI_SP_NAME_LENGTH = "Tên loại sản phẩm quá dài"
    LOAI_SP_NAME_EXISTED = "Tên loại sản phẩm đã tồn tại"
    LOAI_SP_INVALID_ID = "ID loại sản phẩm không hợp lệ"
    SAN_PHAM_OF_LSP_EXITED = "Có sản phẩm thuộc loại sản phẩm vẫn tồn tại!, không cho phép xoá!"

    # DON_VI_TINH - 3xxx
    DVT_NOT_FOUND = "Không tìm thấy đơn vị tính"
    DVT_NAME_REQUIRED = "Tên đơn vị tính là bắt buộc"
    DVT_NAME_LENGTH = "Tên đơn vị tính quá dài"
    DVT_NAME_EXISTED = "Tên đơn vị tính đã tồn tại"
    DVT_INVALID_ID = "ID đơn vị tính không hợp lệ"
    DVT_REFERENCE_SAN_PHAM = "Có sản phẩm đang sử dụng đơn vị tính này!"

    # CHI_TIET_SAN_PHAM - 4xxx
    CTSP_NOT_FOUND = "Không tìm thấy chi tiết sản phẩm"
    CTSP_NAME_REQUIRED = "Tên chi tiết sản phẩm là bắt buộc"
    CTSP_NAME_LENGTH = "Tên chi tiết sản phẩm quá dài"
    CTSP_NAME_EXISTED = "Tên chi tiết sản phẩm đã tồn tại"
    CTSP_INVALID_ID = "ID chi tiết sản phẩm không hợp lệ"
    CTSP_PRICE_GRETER_ZERO = "Giá sản phẩm phải lớn hơn 0"
    CTSP_PRICE_LESSER_ZERO = "Giá sản phẩm không thể nhỏ hơn 0"
    CTSP_REFERENCE_CHI_TIET_XUAT_HD = "Chi tiết sản phẩm này có tham chiếu đến hoá đơn xuất hàng!"
    CTSP_REFERENCE_CHI_TIET_NHAP_HD = "Chi tiết sản phẩm này có tham chiếu đến hoá đơn nhập hàng!"
    CTSP_REFERENCE_TON_KHO = "Chi tiết sản phẩm này vẫn còn trong kho và chưa bị xoá!"

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
    ACCOUNT_INVALID = "Tài khoản hoặc mật khẩu không chính xác!"
    USERNAME_LENGTH = "Tên đăng nhập quá dài hoặc quá ngắn"
    USERNAME_EXISTED = "Tên đăng nhập đã tổn tại!"
    PASSWORD_LENGTH = "Mật khẩu quá dài hoặc quá ngắn"
    NHAN_VIEN_NAME_LENGTH = "Họ tên từ 1 đến 255 ký tự"
    NHAN_VIEN_NOT_FOUND = "Không có nhân viên nào hợp lệ!"
    NHAN_VIEN_REFERENCE_HOA_DON_XUAT = "Nhân viên có tham chiếu đến hoá đơn xuất kho"

    #CHUC_VU - 8xxx
    CHUC_VU_NOT_FOUND = "Không có chức vụ này"
    CHUC_VU_NAME_LENGTH = ""
    CHUC_VU_NAME_REQUIRED = ""

    NHA_PHAN_PHOI_NOT_FOUND = "Không tìm thấy nhà phân phối hợp lệ"
    NHA_PHAN_PHOI_NAME_LENGTH = "Tên nhà phân phối từ 1 đến 255 ký tự"
    NHA_PHAN_PHOI_REFERENCE_SAN_PHAM = "Nhà phân phối này còn cung cấp cho các sản phẩm còn kinh doanh"
    NHA_PHAN_PHOI_REFERENCE_HOA_DON_NHAP = "Nhà phân phối này đã từng cung cấp nhập kho!"

    KHO_NOT_FOUND = "Không tìm thấy kho hợp lệ"
    KHO_REFERENCE_HOA_DON_NHAP = "Kho có tham chiếu đến hoá đơn nhập kho"
    KHO_REFERENCE_HOA_DON_XUAT = "Kho có tham chiếu đến hoá đơn xuất kho"
    KHO_NOT_QUANTITY_FOR_RETURNS = "Số lượng sản phẩm trả hàng vượt quá số lượng mua hàng!"
    KHO_NOT_QUANTITY_FOR_SALE = "Lô hàng không đủ số lượng để bán cho sản phẩm!"
    KHO_NOT_EXISTED_SKU = "Kho không tồn tại mã lô hàng!"
    #NHAP_KHO - 9xxx
    # NHAP_KHO_WRONG_TONG_TIEN = "Tổng tiền gửi về không khớp so vơi"

    HOA_DON_NHAP_PREPAID_LESS_ZERO = "Số tiền trả trước phải lớn hơn 0!"
    HOA_DON_NHAP_PREPAID_GREATER_TOTAL_MONEY = "Số tiền trả trước lớn hơn tổng tiền thanh toán!"
    HOA_DON_NHAP_PREPAID_NOT_SAME = "Số tiền trả trước gửi về không giống nhau!"
    HOA_DON_NHAP_TOTAL_MONEY_NOT_SAME = "Tổng tiền gửi về không giống nhau!"
    HOA_DON_XUAT_TOTAL_MONEY_NOT_SAME = "Tổng tiền gửi về không giống nhau!"
    INVALID_GIFT_FLAG = "Giá trị 'là quà tặng không hợp lệ!'"
    HOA_DON_NHAP_SL_TRA_GREATED_THAN_SO_LUONG_SALE = "Số lượng trả của sản phẩm này lớn hơn số lượng mua!"
    #CHUC_VU - 11xx
    # CHUC_VU_NOT_FOUND = "Không tìm thấy chức vụ!"
    # CHUC_NANG_NOT_FOUND = "Không tìm thấy chức năng!"

    HOA_DON_XUAT_NOT_FOUND = "Không tìm thấy hoá đơn xuất kho"
    HOA_DON_XUAT_NOT_STATUS = "Không có trạng thái này"
    HOA_DON_XUAT_SO_LUONG_BAN_NOT_SAME = "Số lượng bán gửi về không giống với tính toán!"

    #QUYEN HAN
    POWERLESS = "Không có quyền hạn để sử dụng chức năng này!"

    #KHACH HANG - 15xx
    KHACH_HANG_NOT_FOUND = "Không tìm thấy khách hàng này!"
    KHACH_HANG_REFERENCE_HOA_DON_XUAT = "Khách hàng này có tham chiếu đến một hoá đơn xuất kho!"
    
def get_error_response(error_code: ERROR_CODES, result = None, field_error = None):
    """Trả về response JSON chứa errorCode và message tương ứng"""
    field_error_message = field_error if field_error else ''
    message = field_error_message + (MESSAGES[error_code.name].value if error_code.name in MESSAGES.__members__ else "Lỗi không xác định")
    
    return jsonify({
        "error": error_code.value,
        "message": message,
        "data": result
    })