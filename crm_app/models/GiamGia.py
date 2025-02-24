from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, Float
from datetime import datetime

class GiamGia(BaseModel):
    __tablename__ = 'loai_giam_gia'
    ten = Column(String(255), nullable = False)
    gia_tri = Column(Float, default = 0)
    created_at = Column(TIMESTAMP, default = datetime.now())
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    def __str__(self):
        return str(self.id)
