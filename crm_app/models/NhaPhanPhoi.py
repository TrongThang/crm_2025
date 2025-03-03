from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime
from crm_app.models.SanPhamNhaPhanPhoi import SanPhamNhaPhanPhoi

class NhaPhanPhoi(BaseModel):
    __tablename__ = "nha_phan_phoi"
    ten = Column(String, nullable=False)
    dia_chi = Column(TEXT, default='')
    dien_thoai = Column(String(12), default='')
    email = Column(String(255), default='')

    hoa_dons = relationship("HoaDonNhapKho", back_populates="nha_phan_phoi")

    san_pham_nha_phan_phois = relationship("SanPhamNhaPhanPhoi", back_populates="nha_phan_phoi")
    san_phams = relationship("SanPham", secondary="san_pham_nha_phan_phoi", back_populates="nha_phan_phois")
    
    def __str__ (self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'ID': self.id,
            'ten': self.ten,
            'dia_chi': self.dia_chi,
            'dien_thoai': self.dien_thoai,
            'email': self.email,
            'CreatedAt': self.created_at,
            'UpdatedAt': self.updated_at,
            'DeletedAt': self.deleted_at,
        }