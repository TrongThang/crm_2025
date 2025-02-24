from crm_app.models.BaseModel import BaseModel
from sqlalchemy import DateTime, String, Column, Float, TIMESTAMP
from datetime import datetime

class BaoHanh(BaseModel):
    __tablename__ = 'thoi_gian_bao_hanh'
    ten = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP, default = datetime.now())
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    def __str__(self):
        return str(self.id)
