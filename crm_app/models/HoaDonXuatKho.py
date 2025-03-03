from crm_app.models.BaseModel import BaseModel
from sqlalchemy import Column, INT, DateTime, Float, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from datetime import datetime

class HoaDonXuatKho(BaseModel):
    __tablename__ = "hoa_don_xuat_kho"
    khach_hang_id = Column(INT, ForeignKey("nha_phan_phoi.id"), nullable=False)
    nv_giao_hang_id = Column(INT, ForeignKey("nha_phan_phoi.id"), nullable=False)
    nv_sale_id = Column(INT, ForeignKey("nha_phan_phoi.id"), nullable=False)
    ngay_xuat = Column(DateTime)
    tong_tien = Column(Float)
    tra_truoc = Column(Float, default=0)
    ghi_chu = Column(TEXT, default='')

    nha_phan_phoi = relationship("NhaPhanPhoi", back_populates="hoa_dons")
    khos = relationship("Kho", back_populates="hoa_dons")
    chi_tiet_hoa_don_nhap_khos = relationship("ChiTietNhapKho", back_populates="hoa_don_nhap_kho")
    
    def __str__ (self):
        return str(self.id)