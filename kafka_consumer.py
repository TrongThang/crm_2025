from kafka import KafkaConsumer
import json

def process_message(message):
    topic = message.topic  # Không cần gọi hàm topic()
    data = message.value  # kafka-python đã giải mã sẵn JSON nếu dùng value_deserializer

    if topic == "hoa_don_nhap_kho":
        print(f"✅ Hóa đơn nhập kho mới: {data}")
        # Xử lý cập nhật dữ liệu hóa đơn (lưu log, gửi thông báo, cập nhật báo cáo...)

    elif topic == "chi_tiet_hoa_don_nhap_kho":
        print(f"🛒 Chi tiết hóa đơn nhập kho: {data}")
        
        # Xử lý cập nhật sản phẩm, kho hàng...

consumer = KafkaConsumer(
    "hoa_don_nhap_kho",
    "chi_tiet_hoa_don_nhap_kho",
    bootstrap_servers="localhost:9092",
    group_id="hoa_don_group",
    auto_offset_reset="earliest",  # Đọc từ đầu nếu chưa có offset
    enable_auto_commit=True,  # Kafka sẽ tự động commit offset sau khi đọc xong
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))  # Tự động decode JSON
)

print("Consumer đang lắng nghe sự kiện...")

for msg in consumer:
    try:
        process_message(msg)
    except Exception as e:
        print(f"❌ Lỗi xử lý message: {e}")