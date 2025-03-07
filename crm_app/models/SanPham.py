from crm_app.models.BaseModel import BaseModel
from sqlalchemy import TIMESTAMP, String, Column, INT, Float, TEXT, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from crm_app.models.SanPhamNhaPhanPhoi import SanPhamNhaPhanPhoi

class SanPham(BaseModel):
    __tablename__ = 'san_pham'
    ten = Column(String(255), nullable= False)
    upc = Column(String(255))
    hinh_anh = Column(String(max))
    vat = Column(Float)
    mo_ta = Column(TEXT)
    trang_thai = Column(BOOLEAN, default=True)
    loai_san_pham_id = Column(INT, ForeignKey("loai_san_pham.id"))
    don_vi_tinh_id = Column(INT, ForeignKey("don_vi_tinh.id"))
    loai_giam_gia_id = Column(INT, ForeignKey("loai_giam_gia.id"))
    thoi_gian_bao_hanh_id = Column(INT, ForeignKey("thoi_gian_bao_hanh.id"))

    loai_san_pham = relationship("LoaiSanPham", back_populates="san_phams")
    don_vi_tinh = relationship("DonViTinh", back_populates="san_phams")
    loai_giam_gia = relationship("GiamGia", back_populates="san_phams")
    thoi_gian_bao_hanh = relationship("BaoHanh", back_populates="san_phams") 

    san_pham_nha_phan_phois = relationship("SanPhamNhaPhanPhoi", back_populates="san_pham")
    nha_phan_phois = relationship("NhaPhanPhoi", secondary="san_pham_nha_phan_phoi", back_populates="san_phams")
    chi_tiet_hoa_don_nhap_khos = relationship("ChiTietNhapKho", back_populates="san_pham")
    chi_tiet_hoa_don_xuat_khos = relationship("ChiTietXuatKho", back_populates="san_pham")
    def __str__(self):
        return str(self.id)
    

    def delete():
        
        pass
    
    