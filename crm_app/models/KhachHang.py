from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime
from crm_app.models.SanPhamNhaPhanPhoi import SanPhamNhaPhanPhoi

class KhachHang(BaseModel):
    __tablename__ = "khach_hang"
    ho_ten = Column(String(255), nullable=False)
    dia_chi = Column(TEXT, default='')
    dien_thoai = Column(String(12), default='')

    # hoa_don_xuats = relationship("HoaDonXuatKho", back_populates="khach_hang")
    
    def __str__ (self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'ID': self.id,
            'ho_ten': self.ho_ten,
            'dia_chi': self.dia_chi,
            'dien_thoai': self.dien_thoai,
            'CreatedAt': self.created_at,
            'UpdatedAt': self.updated_at,
            'DeletedAt': self.deleted_at,
        }