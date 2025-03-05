import pdfkit

def generate_invoice_html(hoa_don_id, khach_hang, san_pham_list, tong_tien):
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #333; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        <h1>HÓA ĐƠN XUẤT KHO - {hoa_don_id}</h1>
        <p><strong>Khách hàng:</strong> {khach_hang['ten']}</p>
        <p><strong>Ngày xuất:</strong> {khach_hang['ngay_xuat']}</p>
        <table>
            <tr>
                <th>Tên sản phẩm</th>
                <th>Số lượng</th>
                <th>Giá</th>
            </tr>
    """
    for sp in san_pham_list:
        html_content += f"""
        <tr>
            <td>{sp['ten_san_pham']}</td>
            <td>{sp['so_luong']}</td>
            <td>{sp['gia_ban']} VNĐ</td>
        </tr>
        """
    
    html_content += f"""
        </table>
        <h2>Tổng tiền: {tong_tien} VNĐ</h2>
    </body>
    </html>
    """
    
    file_name = f"hoadon_{hoa_don_id}.pdf"
    pdfkit.from_string(html_content, file_name)
    return file_name
