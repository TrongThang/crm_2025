
def check_stock():
    for msg in consumer:
        data = msg.value
        order_id = data["order_id"]
        product_id = data["product_id"]
        quantity = data["quantity"]
        user_id = data["user_id"]

        inventory = Inventory.query.filter_by(product_id=product_id).with_for_update().first()

        if inventory and inventory.stock >= quantity:
            # Nếu đủ hàng, gửi xác nhận để tạo hoá đơn
            producer.send("order_create", value=data)
        else:
            # Nếu không đủ hàng, gửi thông báo từ chối đơn hàng
            producer.send("order_failed", value={"order_id": order_id, "reason": "Out of stock"})

        db.session.commit()