from crm_app.models.BaseModel import BaseModel
from sqlalchemy import DateTime, String, Column, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

class BaoHanh(BaseModel):
    __tablename__ = 'thoi_gian_bao_hanh'
    ten = Column(String(255), nullable = False, unique=True)

    san_phams = relationship("SanPham", back_populates="thoi_gian_bao_hanh")

    def __str__(self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'ID': self.id,
            'ten': self.ten,
            'CreatedAt': self.created_at,
            'UpdatedAt': self.updated_at,
            'DeletedAt': self.deleted_at,
        }