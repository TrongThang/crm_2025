from BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT
from datetime import datetime

class SanPham(BaseModel):
    __tablename__ = 'san_pham'
    ten = Column(String(255), nullable= False)
    upc = Column(String(255))
    loai_san_pham_id = Column(INT)
    hinh_anh = Column(String(255))
    don_vi_tinh_id = Column(INT)
    vat = Column(Float)
    mo_ta = Column(TEXT)
    trang_thai = Column(BOOLEAN, default=True)
    loai_giam_gia_id = Column(INT)
    thoi_gian_bao_hanh_id = Column(INT)
    created_at = Column(TIMESTAMP, default = datetime.now)
    updated_at = Column(TIMESTAMP, default = datetime.now, onupdate=datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)

    def __str__(self):
        return str(self.id)