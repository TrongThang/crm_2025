from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from datetime import datetime

class Quyen(BaseModel):
    __tablename__ = "chuc_vu"
    chuc_vu_id = Column(INT, nullable=False)
    chuc_nane_id = Column(INT)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    created_at = Column(TIMESTAMP)

    def __str__ (self):
        return str(self.id)