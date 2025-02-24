from BaseModel import BaseModel
from sqlalchemy import DateTime, String, Column, Float, TIMESTAMP, INT, BOOLEAN
from datetime import datetime

class ChiTietSanPham(BaseModel):
    __tablename__ = 'chi_tiet_san_pham'
    san_pham_id = Column(INT)
    ten_phan_loai = Column(String(255), nullable= False)
    hinh_anh = Column(String(255), nullable= False)
    gia_nhap = Column(Float)
    gia_ban = Column(String(255))
    trang_thai = Column(BOOLEAN, default=True)
    khong_phan_loai = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP, default = datetime.now())
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    def __str__(self):
        return str(self.id)