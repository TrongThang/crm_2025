from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column
from sqlalchemy.orm import relationship
from datetime import datetime

class DonViTinh(BaseModel):
    __tablename__ = 'don_vi_tinh'
    ten = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP, default = datetime.now())
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    san_phams = relationship("SanPham", back_populates="don_vi_tinh")

    def __str__(self):
        return str(self.id)