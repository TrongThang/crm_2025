from flask_restful import Api
from flask import Blueprint
from crm_app.controllers import (
    DonViTinhController,
    GiamGiaController,
    BaoHanhController,
    LoaiSanPhamController,
    SanPhamController,
)
from crm_app.controllers.AcountController import LoginController, RegisterController, GetMeController
from crm_app.controllers.QuyenChucVuController import QuyenChucVuController
from crm_app.controllers.ChucVuController import ChucVuController 
from crm_app.controllers.KhoController import KhoController, TonKhoController
from crm_app.controllers.HoaDonNhapKhoController import HoaDonNhapKhoController
from crm_app.controllers.HoaDonXuatKhoController import HoaDonXuatKhoController, ChiTietXuatKhoController
from crm_app.controllers.NhaPhanPhoiController import NhaPhanPhoiController
from crm_app.controllers.KhachHangController import KhachHangController
from crm_app.controllers.NhanVienController import NhanVienController

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
        (GetMeController, "/thong-tin-nhan-vien"),
        (RegisterController, "/dang-ki"),
        (NhaPhanPhoiController, "/nha-phan-phoi"),
        (NhanVienController, "/nhan-vien"),
        (KhachHangController, "/khach-hang"),
        (QuyenChucVuController, "/quyen-han"),
        (ChucVuController, "/chuc-vu"),
        (HoaDonNhapKhoController, "/hoa-don-nhap-kho"),
        (KhoController, "/kho"),
        (TonKhoController, "/ton-kho"),
        (HoaDonXuatKhoController, "/hoa-don-xuat-kho"),
        (ChiTietXuatKhoController, "/xuat-kho/chi-tiet"),
    ]

    # Đăng ký route vào API
    for controller, route in routes:
        api.add_resource(controller, route)

    app.register_blueprint(api_blueprint)
    
    return api
