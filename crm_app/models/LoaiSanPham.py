from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT
from sqlalchemy.orm import relationship
from datetime import datetime

class LoaiSanPham(BaseModel):
    __tablename__ = 'loai_san_pham'
    ten = Column(String(255), nullable= False, unique=True)
    hinh_anh = Column(String(255))

    san_phams = relationship("SanPham", back_populates="loai_san_pham")

    def __str__(self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'ID': self.id,
            'ten': self.ten,
            'hinh_anh': self.hinh_anh,
            'CreatedAt': self.created_at,
            'UpdatedAt': self.updated_at,
            'DeletedAt': self.deleted_at,
        }