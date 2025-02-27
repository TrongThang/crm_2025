from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class SanPham(BaseModel):
    __tablename__ = 'san_pham'
    ten = Column(String(255), nullable= False)
    upc = Column(String(255))
    hinh_anh = Column(String(255))
    vat = Column(Float)
    mo_ta = Column(TEXT)
    trang_thai = Column(BOOLEAN, default=True)
    loai_san_pham_id = Column(INT, ForeignKey("loai_san_pham.id"))
    don_vi_tinh_id = Column(INT, ForeignKey("don_vi_tinh.id"))
    loai_giam_gia_id = Column(INT, ForeignKey("loai_giam_gia.id"))
    thoi_gian_bao_hanh_id = Column(INT, ForeignKey("thoi_gian_bao_hanh.id"))

    loai_san_pham = relationship("LoaiSanPham", back_populates="san_phams")
    don_vi_tinh = relationship("DonViTinh", back_populates="san_phams")
    loai_giam_gia = relationship("GiamGia", back_populates="san_phams")
    thoi_gian_bao_hanh = relationship("BaoHanh", back_populates="san_phams") 


    def __str__(self):
        return str(self.id)
    
    