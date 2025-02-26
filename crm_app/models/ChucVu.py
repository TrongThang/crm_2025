from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from datetime import datetime

class ChucVu(BaseModel):
    __tablename__ = "chuc_vu"
    ten = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    created_at = Column(TIMESTAMP)

    def __str__ (self):
        return str(self.id)