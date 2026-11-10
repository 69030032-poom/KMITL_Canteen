import sqlite3
import uuid
from pathlib import Path
from PIL import Image, ImageOps
from Backend import database, users


def read_menus():
    shop = users.get_my_shop()
    connection = database.connect_database()
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute('SELECT * FROM menu_items WHERE shop_id=? ORDER BY name', (shop['shop_id'],))]
    finally:
        connection.close()


def read_choices(menu_id):
    shop = users.get_my_shop()
    connection = database.connect_database()
    try:
        owner = connection.execute('SELECT shop_id FROM menu_items WHERE menu_id=?', (menu_id,)).fetchone()
        if not owner or owner[0] != shop['shop_id']:
            raise ValueError('ไม่มีสิทธิ์แก้เมนูนี้')
        variants = connection.execute('SELECT name, price FROM menu_variants WHERE menu_id=? AND is_available=1', (menu_id,)).fetchall()
        options = connection.execute('SELECT group_name, name, extra_price FROM menu_item_options WHERE menu_id=?', (menu_id,)).fetchall()
        return variants, options
    finally:
        connection.close()


def save_menu(menu_id, name, price, available, variants, options, image_file=None):
    shop = users.get_my_shop()
    name = name.strip()
    if not name or len(name)>100:
        raise ValueError('กรอกชื่อเมนู 1–100 ตัวอักษร')
    if type(price) is not int or price<0:
        raise ValueError('ราคาต้องเป็นจำนวนเต็มบาทตั้งแต่ 0')
    for row in variants + options:
        if any(not str(value).strip() for value in row) or type(row[-1]) is not int or row[-1]<0:
            raise ValueError('กรอกชื่อตัวเลือกและราคาที่ไม่ติดลบ')
    image_path = None
    if image_file:
        with Image.open(image_file) as image:
            image = ImageOps.exif_transpose(image).convert('RGB')
            image.thumbnail((1200,1200))
            folder = database.database_file.parent / 'menu_images'
            folder.mkdir(exist_ok=True)
            target = folder / (uuid.uuid4().hex + '.jpg')
            image.save(target, 'JPEG', quality=88)
            image_path = target.name
    connection = database.connect_database()
    try:
        with connection:
            if menu_id is None:
                cursor = connection.execute('INSERT INTO menu_items(shop_id,name,price,is_available,image_path) VALUES (?,?,?,?,?)', (shop['shop_id'],name,price,int(available),image_path or ''))
                menu_id = cursor.lastrowid
            else:
                cursor = connection.execute('UPDATE menu_items SET name=?,price=?,is_available=? WHERE menu_id=? AND shop_id=?', (name,price,int(available),menu_id,shop['shop_id']))
                if cursor.rowcount != 1:
                    raise ValueError('ไม่มีสิทธิ์แก้เมนูนี้')
                if image_path:
                    connection.execute('UPDATE menu_items SET image_path=? WHERE menu_id=?', (image_path,menu_id))
            connection.execute('DELETE FROM menu_variants WHERE menu_id=?', (menu_id,))
            connection.execute('DELETE FROM menu_item_options WHERE menu_id=?', (menu_id,))
            connection.executemany('INSERT INTO menu_variants(menu_id,name,price) VALUES (?,?,?)', [(menu_id,*row) for row in variants])
            connection.executemany('INSERT INTO menu_item_options(menu_id,group_name,name,extra_price) VALUES (?,?,?,?)', [(menu_id,*row) for row in options])
        return menu_id
    finally:
        connection.close()


def save_hours(opening, closing, capacity, active):
    from datetime import datetime
    shop = users.get_my_shop()
    for value in (opening,closing):
        try:
            if datetime.strptime(value,'%H:%M').strftime('%H:%M') != value:
                raise ValueError()
        except ValueError:
            raise ValueError('เวลาใช้รูปแบบ HH:MM เช่น 06:45')
    if opening>=closing or not 1<=capacity<=1000:
        raise ValueError('เวลาปิดต้องหลังเวลาเปิด และจำนวนคิวต้องอยู่ระหว่าง 1–1000')
    connection = database.connect_database()
    try:
        with connection:
            connection.execute('UPDATE shops SET opening_time=?,closing_time=?,slot_capacity=?,is_active=? WHERE shop_id=?', (opening,closing,capacity,int(active),shop['shop_id']))
    finally:
        connection.close()
