from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from datetime import datetime

class ChucNang(BaseModel):
    __tablename__ = "chuc_nang"
    ten = Column(String(255), nullable=Fasle)
    created_at = Column(TIMESTAMP, default=datetime.now)
    code = Column(String(255))
    type = Column(String(255))
    show_in_menu = Column(String(255))
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    created_at = Column(TIMESTAMP)

    def __str__ (self):
        return str(self.id)