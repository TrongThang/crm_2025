from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from datetime import datetime

class ChucNang(BaseModel):
    __tablename__ = "chuc_nang"
    ten          = Column(String(255), nullable=False, unique=True)
    code         = Column(String(255), unique=True)
    type         = Column(String(255))
    show_in_menu = Column(String(255)) 

    def __str__ (self):
        return str(self.id)