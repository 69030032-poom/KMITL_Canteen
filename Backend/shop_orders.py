import sqlite3

from Backend import database, users, scheduling


status_names = {
    'expired': 'เลยเวลารับ — หมดอายุการแจ้งชำระ',
    'pending': 'ออเดอร์เก่า — ยังไม่ผ่านขั้นแจ้งชำระ',
    'awaiting_payment_review': 'รอตรวจสอบการชำระเงิน',
    'payment_rejected': 'หลักฐานชำระไม่ผ่าน',
    'paid': 'ตรวจรับเงินแล้ว รอร้านรับออเดอร์',
    'preparing': 'กำลังเตรียมอาหาร',
    'ready': 'พร้อมรับอาหาร',
    'completed': 'รับอาหารแล้ว',
    'cancelled': 'ลูกค้ายกเลิกคำสั่งซื้อ',
}

next_statuses = {
    'awaiting_payment_review': ('paid', 'payment_rejected'),
    'payment_rejected': ('awaiting_payment_review',),
    'paid': ('preparing',),
    'preparing': ('ready',),
    'ready': ('completed',),
}


def read_orders(canteen_name, shop_name):
    scheduling.refresh_overdue()
    user = users.require_user('shop')
    shop = users.get_my_shop()
    if (canteen_name, shop_name) != (shop['canteen_name'], shop['shop_name']):
        return []
    connection = database.connect_database()
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute("""
            SELECT orders.*, COALESCE(SUM(unit_price * quantity), 0) AS total
            FROM orders LEFT JOIN order_items USING(order_id)
            WHERE orders.shop_id = ?
            GROUP BY orders.order_id ORDER BY orders.order_id DESC
        """, (user['shop_id'],))
        return [dict(row) for row in rows]
    finally:
        connection.close()


def read_items(order_id, canteen_name, shop_name):
    scheduling.refresh_overdue()
    user = users.require_user('shop')
    shop = users.get_my_shop()
    if (canteen_name, shop_name) != (shop['canteen_name'], shop['shop_name']):
        return []
    connection = database.connect_database()
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute("""
            SELECT order_items.* FROM order_items
            JOIN orders USING(order_id)
            WHERE order_id = ? AND orders.shop_id = ?
            ORDER BY item_id
        """, (order_id, user['shop_id']))
        return [dict(row) for row in rows]
    finally:
        connection.close()


def change_status(order_id, canteen_name, shop_name, old_status, new_status):
    if new_status not in next_statuses.get(old_status, ()):
        raise ValueError('ไม่สามารถข้ามขั้นตอนหรือย้อนสถานะนี้ได้')
    scheduling.refresh_overdue()
    user = users.require_user('shop')
    shop = users.get_my_shop()
    if (canteen_name, shop_name) != (shop['canteen_name'], shop['shop_name']):
        raise ValueError('บัญชีนี้ไม่มีสิทธิ์จัดการร้านที่เลือก')
    connection = database.connect_database()
    try:
        with connection:
            cursor = connection.execute("""
                UPDATE orders SET status = ?
                WHERE order_id = ? AND orders.shop_id = ? AND status = ?
            """, (new_status, order_id, user['shop_id'], old_status))
            if cursor.rowcount != 1:
                raise ValueError('ไม่พบออเดอร์ของร้านนี้ หรือสถานะเปลี่ยนแล้ว กรุณารีเฟรช')
    finally:
        connection.close()
