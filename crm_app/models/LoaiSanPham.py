from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT
from sqlalchemy.orm import relationship
from datetime import datetime

class LoaiSanPham(BaseModel):
    __tablename__ = 'loai_san_pham'
    ten = Column(String(255), nullable= False)
    hinh_anh = Column(String(255))
    created_at = Column(TIMESTAMP, default = datetime.now)
    updated_at = Column(TIMESTAMP, default = datetime.now, onupdate=datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)

    san_phams = relationship("SanPham", back_populates="loai_san_pham")

    def __str__(self):
        return str(self.id)