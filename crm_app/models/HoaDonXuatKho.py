from crm_app.models.BaseModel import BaseModel
from sqlalchemy import Column, INT, DateTime, Float, ForeignKey, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime

class HoaDonXuatKho(BaseModel):
    __tablename__ = "hoa_don_xuat_kho"
    so_hoa_don = Column(INT, nullable=False)
    ma_hoa_don = Column(INT, nullable=False)
    khach_hang_id = Column(INT, ForeignKey("khach_hang.id"), nullable=False)
    nhan_vien_giao_hang_id = Column(INT, ForeignKey("nhan_vien.id"), nullable=False)
    nhan_vien_sale_id = Column(INT, ForeignKey("nhan_vien.id"), nullable=False)
    ngay_xuat = Column(DateTime)
    tong_tien = Column(Float, default=0)
    vat = Column(Float, default=0)
    tra_truoc = Column(Float, default=0)
    con_lai = Column(Float, default=0)
    thanh_tien = Column(Float, default=0)
    tong_gia_nhap = Column(Float, default=0)
    loi_nhuan = Column(Float, default=0)
    da_giao_hang = Column(BOOLEAN, default=False)
    loai_chiet_khau = Column(TEXT, default='')
    gia_tri_chiet_khau = Column(TEXT, default='')
    ghi_chu = Column(TEXT, default='')

    # chi_tiet_hoa_don_xuat_khos = relationship("ChiTietXuatKho", back_populates="hoa_don_xuat_kho")
    
    def __str__ (self):
        return str(self.id)