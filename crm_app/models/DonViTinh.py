from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column
from datetime import datetime

class DonViTinh(BaseModel):
    __tablename__ = 'don_vi_tinh'
    ten = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP, default = datetime.now())
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    def __str__(self):
        return str(self.id)