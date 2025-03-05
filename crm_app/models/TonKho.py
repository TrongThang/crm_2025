from crm_app.models.BaseModel import BaseModel
from sqlalchemy import Column, INT, DateTime, Float, ForeignKey, TEXT, String
from sqlalchemy.orm import relationship

class TonKho(BaseModel):
    __tablename__ = "ton_kho"
    san_pham_id = Column(INT, ForeignKey("san_pham.id"), nullable=False)
    ctsp_id = Column(INT, ForeignKey("chi_tiet_san_pham.id"), nullable=False)
    sku = Column(String(255),default='')
    so_luong_ton = Column(INT, default=0)

    # chi_tiet_hoa_don_xuat_khos = relationship("ChiTietXuatKho", back_populates="hoa_don_xuat_kho")
    
    def __str__ (self):
        return str(self.id)