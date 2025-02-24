from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT
from datetime import datetime

class LoaiSanPham(BaseModel):
    __tablename__ = 'loai_san_pham'
    ten = Column(String(255), nullable= False)
    hinh_anh = Column(String(255))
    created_at = Column(TIMESTAMP, default = datetime.now)
    updated_at = Column(TIMESTAMP, default = datetime.now, onupdate=datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)

    def __str__(self):
        return str(self.id)