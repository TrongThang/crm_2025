from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class GiamGia(BaseModel):
    __tablename__ = 'loai_giam_gia'
    ten = Column(String(255), nullable = False, unique=True)
    gia_tri = Column(Float, default = 0)

    san_phams = relationship("SanPham", back_populates="loai_giam_gia")

    def __str__(self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'ID': self.id,
            'ten': self.ten,
            'gia_tri': self.gia_tri,
            'CreatedAt': self.created_at,
            'UpdatedAt': self.updated_at,
            'DeletedAt': self.deleted_at,
        }