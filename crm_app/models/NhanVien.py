from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN
from datetime import datetime

class NhanVien(BaseModel):
    __tablename__ = 'nhan_vien'
    ten_dang_nhap = Column(String(255), nullable= False)
    mat_khau = Column(String(255))
    ho_ten = Column(INT)
    email = Column(String(255))
    dien_thoai = Column(INT)
    dia_chi = Column(String(255))
    avatar = Column(TEXT)
    chuc_vu_id = Column(BOOLEAN, default=True)
    created_at = Column(TIMESTAMP, default = datetime.now)
    updated_at = Column(TIMESTAMP, default = datetime.now, onupdate=datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)

    def __str__(self):
        return str(self.id)