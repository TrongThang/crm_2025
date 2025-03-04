from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, DateTime, TEXT, BOOLEAN, Float, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class ChiTietXuatKho(BaseModel):
    __tablename__ = "chi_tiet_hoa_don_xuat_kho"
    hoa_don_id = Column(INT, ForeignKey("hoa_don_nhap_kho.id"), nullable=False)
    san_pham_id = Column(INT, ForeignKey("san_pham.id"), nullable=False)
    ctsp_id = Column(INT, ForeignKey("chi_tiet_san_pham.id"), nullable=False)
    lo = Column(String(255), unique=True)
    so_luong = Column(INT, default=0)
    don_vi_tinh = Column(String(255))
    gia_ban = Column(Float, default=0)
    chiet_khau = Column(Float, default=0)
    thanh_tien = Column(Float, default=0)
    la_qua_tang = Column(BOOLEAN, default=0)

    # hoa_don_xuat_kho = relationship("HoaDonXuatKho", back_populates="chi_tiet_hoa_don_xuat_khos")
    san_pham = relationship("SanPham", back_populates="chi_tiet_hoa_don_xuat_khos")
    chi_tiet_san_pham = relationship("ChiTietSanPham", back_populates="chi_tiet_hoa_don_xuat_khos")
    
    def __str__ (self):
        return str(self.id)