from crm_app.models.BaseModel import BaseModel
from sqlalchemy import Column, INT, DateTime, Float, ForeignKey, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime

class HoaDonNhapKho(BaseModel):
    __tablename__ = "hoa_don_nhap_kho"
    so_hoa_don = Column(INT, nullable=False)
    ma_hoa_don = Column(INT, nullable=False)
    nha_phan_phoi_id = Column(INT, ForeignKey("nha_phan_phoi.id"), nullable=False)
    kho_id = Column(INT, ForeignKey("kho.id"), nullable=False, )
    ngay_nhap = Column(DateTime)
    tong_tien = Column(Float)
    tra_truoc = Column(Float, default=0)
    con_lai = Column(Float, default=0)
    khoa_don = Column(BOOLEAN, default=False)
    ghi_chu = Column(TEXT, default='')

    nha_phan_phoi = relationship("NhaPhanPhoi", back_populates="hoa_dons")
    khos = relationship("Kho", back_populates="hoa_dons")
    chi_tiet_hoa_don_nhap_khos = relationship("ChiTietNhapKho", back_populates="hoa_don_nhap_kho")
    
    def __str__ (self):
        return str(self.id)