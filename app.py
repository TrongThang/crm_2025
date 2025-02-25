from crm_app import *
from flask_restful import Api
from crm_app.controllers import DonViTinhController, GiamGiaController, BaoHanhController, LoaiSanPhamController, SanPhamController

api = Api(app)

api.add_resource(DonViTinhController.DonViTinhController, "/api/don-vi-tinh")
api.add_resource(GiamGiaController.GiamGiaController, "/api/giam-gia")
api.add_resource(BaoHanhController.BaoHanhController, "/api/bao-hanh")
api.add_resource(LoaiSanPhamController.LoaiSanPhamController, "/api/loai-san-pham")
api.add_resource(SanPhamController.SanPhamController, "/api/san-pham")
api.add_resource(SanPhamController.ChiTietSanPhamController, "/api/chi-tiet-san-pham")

if __name__ == '__main__':
    app.run(debug=True)