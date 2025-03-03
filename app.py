from crm_app import *
from flask_restful import Api
from crm_app.controllers import DonViTinhController, GiamGiaController, BaoHanhController, LoaiSanPhamController, SanPhamController
from crm_app.controllers.AcountController import LoginController, RegisterController 
from crm_app.controllers.QuyenChucVuController import QuyenChucVuController
from crm_app.controllers.HoaDonNhapKhoController import HoaDonNhapKhoController
from crm_app.controllers.NhaPhanPhoiController import NhaPhanPhoiController
from crm_app.controllers.KhachHangController import KhachHangController

api = Api(app)

api.add_resource(DonViTinhController.DonViTinhController, "/api/don-vi-tinh")
api.add_resource(GiamGiaController.GiamGiaController, "/api/giam-gia")
api.add_resource(BaoHanhController.BaoHanhController, "/api/bao-hanh")
api.add_resource(LoaiSanPhamController.LoaiSanPhamController, "/api/loai-san-pham")
api.add_resource(SanPhamController.SanPhamController, "/api/san-pham")
api.add_resource(LoginController, "/api/login")
api.add_resource(RegisterController, "/api/register")


api.add_resource(NhaPhanPhoiController, "/api/nha-phan-phoi")
api.add_resource(KhachHangController, "/api/khach-hang")
api.add_resource(QuyenChucVuController, "/api/quyen-han")
api.add_resource(HoaDonNhapKhoController, "/api/nhap-kho")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5007, threaded=True)