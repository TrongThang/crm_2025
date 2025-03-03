from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
 

class SanPhamNhaPhanPhoi(BaseModel):
    __tablename__ = "san_pham_nha_phan_phoi"
    nha_phan_phoi_id = Column(INT, ForeignKey("nha_phan_phoi.id"), primary_key=True)
    san_pham_id = Column(INT, ForeignKey("san_pham.id"), primary_key=True)
    
    nha_phan_phoi = relationship("NhaPhanPhoi", back_populates="san_pham_nha_phan_phois")
    san_pham = relationship("SanPham", back_populates="san_pham_nha_phan_phois")

    def __str__ (self):
        return str(self.id)