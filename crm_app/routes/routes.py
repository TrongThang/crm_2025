from flask_restful import Api
from flask import Blueprint
from crm_app.controllers import (
    DonViTinhController,
    GiamGiaController,
    BaoHanhController,
    LoaiSanPhamController,
    SanPhamController,
)
from crm_app.controllers.AcountController import LoginController, RegisterController
from crm_app.controllers.QuyenChucVuController import QuyenChucVuController
from crm_app.controllers.HoaDonNhapKhoController import HoaDonNhapKhoController
from crm_app.controllers.HoaDonXuatKhoController import HoaDonXuatKhoController, ChiTietXuatKhoController
from crm_app.controllers.NhaPhanPhoiController import NhaPhanPhoiController
from crm_app.controllers.KhachHangController import KhachHangController

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_blueprint)

def register_routes(app):
    api = Api(api_blueprint)

    routes = [
        (DonViTinhController.DonViTinhController, "/don-vi-tinh"),
        (GiamGiaController.GiamGiaController, "/loai-giam-gia"),
        (BaoHanhController.BaoHanhController, "/thoi-gian-bao-hanh"),
        (LoaiSanPhamController.LoaiSanPhamController, "/loai-san-pham"),
        (SanPhamController.SanPhamController, "/san-pham"),
        (SanPhamController.ChiTietSanPhamController, "/san-pham/chi-tiet"),
        (LoginController, "/dang-nhap"),
        (RegisterController, "/dang-ki"),
        (NhaPhanPhoiController, "/nha-phan-phoi"),
        (KhachHangController, "/khach-hang"),
        (QuyenChucVuController, "/quyen-han"),
        (HoaDonNhapKhoController, "/nhap-kho"),
        (HoaDonXuatKhoController, "/xuat-kho"),
        (ChiTietXuatKhoController, "/xuat-kho/chi-tiet"),
    ]

    # Đăng ký route vào API
    for controller, route in routes:
        api.add_resource(controller, route)

    app.register_blueprint(api_blueprint)
    
    return api
