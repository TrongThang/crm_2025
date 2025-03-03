from crm_app.models.BaseModel import BaseModel
from sqlalchemy import DateTime, String, Column, Float, TIMESTAMP, INT, BOOLEAN
from sqlalchemy.orm import relationship 
from datetime import datetime

class ChiTietSanPham(BaseModel):
    __tablename__ = 'chi_tiet_san_pham'
    san_pham_id = Column(INT)
    ten_phan_loai = Column(String(255), nullable= False, unique=True)
    hinh_anh = Column(String(255), nullable= False)
    gia_nhap = Column(Float)
    gia_ban = Column(String(255))
    so_luong = Column(INT, default=0)
    trang_thai = Column(BOOLEAN, default=True)
    khong_phan_loai = Column(BOOLEAN, default=False)

    chi_tiet_hoa_don_nhap_khos = relationship("ChiTietNhapKho", back_populates="chi_tiet_san_pham")

    def __str__(self):
        return str(self.id)