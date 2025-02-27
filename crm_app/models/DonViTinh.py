from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column
from sqlalchemy.orm import relationship
from datetime import datetime

class DonViTinh(BaseModel):
    __tablename__ = 'don_vi_tinh'
    ten = Column(String(255), nullable = False, unique=True)

    san_phams = relationship("SanPham", back_populates="don_vi_tinh")

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