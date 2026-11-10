from datetime import datetime
from Backend import checkout, database


def refresh_overdue():
    now = datetime.now(checkout.THAI_TIME).strftime('%Y-%m-%d %H:%M')
    connection = database.connect_database()
    try:
        with connection:
            connection.execute("UPDATE orders SET status='expired' WHERE status IN ('awaiting_payment_review','payment_rejected') AND pickup_date || ' ' || pickup_time < ?", (now,))
            connection.execute("UPDATE orders SET is_overdue=1 WHERE status IN ('paid','preparing','ready') AND pickup_date || ' ' || pickup_time < ?", (now,))
    finally:
        connection.close()


def check_slot(connection, shop, date, time):
    if not shop['opening_time'] <= time <= shop['closing_time']:
        raise ValueError(f"ร้านรับอาหารเวลา {shop['opening_time']}–{shop['closing_time']}")
    minute = int(time[:2])*60 + int(time[3:])
    start = minute // 15 * 15
    lower = f'{start//60:02d}:{start%60:02d}'
    end = start + 15
    upper = f'{end//60:02d}:{end%60:02d}'
    count = connection.execute("SELECT count(*) FROM orders WHERE shop_id=? AND pickup_date=? AND pickup_time>=? AND pickup_time<? AND status NOT IN ('cancelled','expired')", (shop['shop_id'],date,lower,upper)).fetchone()[0]
    if count >= shop['slot_capacity']:
        raise ValueError('ช่วงเวลานี้คิวเต็ม กรุณาเลือกช่วงเวลาอื่น')


def check_available(canteen, shop_name, date, time):
    from Backend import catalog
    shop = catalog.get_shop(canteen, shop_name)
    connection = database.connect_database()
    try:
        check_slot(connection, shop, date, time)
    finally:
        connection.close()
