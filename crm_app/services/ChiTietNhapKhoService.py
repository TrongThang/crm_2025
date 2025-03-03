
def get_ct_nhap_kho(hoa_don_id):
    get_table = 'hoa_don_nhap_kho'
    get_attr = """
        nha_phan_phoi.ten as nha_phan_phoi, nha_phan_phoi.id as nha_phan_phoi_id,
        kho.ten as kho, kho.id as kho_id, ngay_nhap, tong_tien
    """
    
    
    return 