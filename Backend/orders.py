import json
import uuid
from Backend import scheduling
from datetime import datetime

from Backend import checkout, database, catalog, users


def cancel_order(order_id):
    user = users.require_user('customer')
    connection = database.connect_database()
    try:
        with connection:
            cursor = connection.execute("""
                UPDATE orders SET status = 'cancelled'
                WHERE order_id = ? AND user_id = ?
                  AND status = 'awaiting_payment_review'
            """, (order_id, user['user_id']))
            if cursor.rowcount != 1:
                raise ValueError('ยกเลิกไม่ได้: ไม่พบคำสั่งซื้อของคุณ หรือสถานะเปลี่ยนแล้ว กรุณาตรวจสอบสถานะล่าสุด')
    finally:
        connection.close()


def check_items(canteen_name, shop_name, items):
    if not items:
        raise ValueError("ตะกร้าว่าง กรุณาเพิ่มอาหารก่อน")
    for item in items:
        if item["canteen"] != canteen_name or item["shop"] != shop_name:
            raise ValueError("หนึ่งคำสั่งซื้อต้องเป็นอาหารจากร้านเดียวกัน")
        quantity = item["quantity"]
        price = item["price"]
        if type(quantity) is not int or quantity < 1:
            raise ValueError("จำนวนอาหารต้องเป็นจำนวนเต็มตั้งแต่ 1 ขึ้นไป")
        if type(price) is not int or price < 0:
            raise ValueError("ราคาอาหารต้องเป็นจำนวนเต็มบาทและไม่ติดลบ")


def insert_order(connection, canteen_name, shop_name, name, phone, pickup_date, pickup_time, user_id, shop_id):
    sql = """
        INSERT INTO orders (
            canteen_name, shop_name, customer_name, phone,
            pickup_date, pickup_time, created_at, status, user_id, shop_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    created_at = datetime.now(checkout.THAI_TIME).isoformat(timespec="seconds")
    values = (
        canteen_name,
        shop_name,
        name.strip(),
        phone.strip(),
        pickup_date,
        pickup_time,
        created_at,
        "awaiting_payment_review",
        user_id,
        shop_id,
    )
    cursor = connection.execute(sql, values)
    return cursor.lastrowid


def insert_order_item(connection, order_id, item):
    sql = """
        INSERT INTO order_items (
            order_id, menu_name, unit_price, quantity, options, note
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    options_text = json.dumps(item["options"], ensure_ascii=False)
    values = (
        order_id,
        item["menu"],
        item["price"],
        item["quantity"],
        options_text,
        item["note"],
    )
    connection.execute(sql, values)


def save_order(canteen_name, shop_name, items, name, phone, pickup_date, pickup_time, request_id=None):
    user = users.require_user('customer')
    request_id = request_id or str(uuid.uuid4())
    payload = json.dumps([canteen_name, shop_name, items, name, phone, pickup_date, pickup_time], ensure_ascii=False, sort_keys=True)
    scheduling.refresh_overdue()
    connection = database.connect_database()
    try:
        with connection:
            connection.execute('BEGIN IMMEDIATE')
            existing = connection.execute('SELECT order_id, request_payload FROM orders WHERE user_id=? AND request_id=?', (user['user_id'],request_id)).fetchone()
            if existing:
                if existing[1] != payload:
                    raise ValueError('รหัสคำขอเดิมมีข้อมูลต่างกัน กรุณาเริ่มสั่งใหม่')
                return existing[0]
            token = catalog._transaction_connection.set(connection)
            try:
                shop = catalog.get_shop(canteen_name, shop_name)
                error = checkout.check_details(name, phone, pickup_date, pickup_time)
                if error:
                    raise ValueError(error)
                scheduling.check_slot(connection, shop, pickup_date, pickup_time)
                check_items(canteen_name, shop_name, items)
                for item in items:
                    catalog.check_cart_item(item)
            finally:
                catalog._transaction_connection.reset(token)
            order_id = insert_order(connection, canteen_name, shop_name, name, phone, pickup_date, pickup_time, user['user_id'], shop['shop_id'])
            connection.execute('UPDATE orders SET request_id=?, request_payload=? WHERE order_id=?', (request_id,payload,order_id))
            for item in items:
                insert_order_item(connection, order_id, item)
        return order_id
    finally:
        connection.close()
