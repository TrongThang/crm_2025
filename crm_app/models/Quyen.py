from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from datetime import datetime

class Quyen(BaseModel):
    __tablename__ = "chuc_vu"
    chuc_vu_id = Column(INT, nullable=False)
    chuc_nane_id = Column(INT)

    def __str__ (self):
        return str(self.id)