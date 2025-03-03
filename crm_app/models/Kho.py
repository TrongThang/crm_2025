from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime

class Kho(BaseModel):
    __tablename__ = "kho"
    ten = Column(String, nullable=False)
    dia_chi = Column(TEXT, default='')

    hoa_dons = relationship("HoaDonNhapKho", back_populates="khos")

    def __str__ (self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'ID': self.id,
            'ten': self.ten,
            'da_chi': self.dia_chi,
            'CreatedAt': self.created_at,
            'UpdatedAt': self.updated_at,
            'DeletedAt': self.deleted_at,
        }