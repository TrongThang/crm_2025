import smtplib
import os
from email.message import EmailMessage

def send_invoice_email(to_email, pdf_path, hoa_don_id):
    msg = EmailMessage()
    msg["Subject"] = f"Hóa đơn xuất kho #{hoa_don_id}"
    msg["From"] = "ikungfu777@gmail.com"
    msg["To"] = to_email
    msg.set_content("Xin chào,\n\nVui lòng kiểm tra file đính kèm để xem hóa đơn xuất kho của bạn.\n\nTrân trọng!")

    # Đính kèm file PDF
    # with open(pdf_path, "rb") as f:
    #     file_data = f.read()
    #     file_name = os.path.basename(pdf_path)
    #     msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Gửi email qua SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("ikungfu777@gmail.com", "password_")
        server.send_message(msg)

    print(f"Email đã gửi đến {to_email} thành công!")


send_invoice_email(to_email="ptthang2910@gmail.com", pdf_path='',hoa_don_id='123')