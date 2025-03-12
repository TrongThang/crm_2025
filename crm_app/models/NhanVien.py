from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN, ForeignKey
from datetime import datetime

class NhanVien(BaseModel):
    __tablename__ = 'nhan_vien'
    ten_dang_nhap = Column(String(255), nullable= False, unique=True)
    mat_khau = Column(String(255))
    ho_ten = Column(String(255))
    email = Column(String(255))
    dien_thoai = Column(String(255))
    dia_chi = Column(String(255))
    avatar = Column(TEXT)
    chuc_vu_id = Column(INT, ForeignKey("chuc_vu.id"))

    def __str__(self):
        return str(self.id)