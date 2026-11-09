-- Run after 03_education_real_shops.sql. Prices transcribed from the shop sign.

PRAGMA foreign_keys = ON;

SAVEPOINT drink_variants;

CREATE TABLE IF NOT EXISTS menu_variants (
    variant_id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL REFERENCES menu_items(menu_id),
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK(typeof(price) = 'integer' AND price >= 0),
    is_available INTEGER NOT NULL DEFAULT 1 CHECK(is_available IN (0, 1)),
    UNIQUE(menu_id, name)
);


INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'เอสเพรสโซ่', 35, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ร้อน', 35 FROM menu_items WHERE name='เอสเพรสโซ่' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('เอสเพรสโซ่ ร้อน', 'เอสเพรสโซ่ร้อน') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 40 FROM menu_items WHERE name='เอสเพรสโซ่' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('เอสเพรสโซ่ เย็น', 'เอสเพรสโซ่เย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 45 FROM menu_items WHERE name='เอสเพรสโซ่' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('เอสเพรสโซ่ ปั่น', 'เอสเพรสโซ่ปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'ลาเต้', 35, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ร้อน', 35 FROM menu_items WHERE name='ลาเต้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ลาเต้ ร้อน', 'ลาเต้ร้อน') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 45 FROM menu_items WHERE name='ลาเต้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ลาเต้ เย็น', 'ลาเต้เย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 50 FROM menu_items WHERE name='ลาเต้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ลาเต้ ปั่น', 'ลาเต้ปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'คาปูชิโน', 35, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ร้อน', 35 FROM menu_items WHERE name='คาปูชิโน' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('คาปูชิโน ร้อน', 'คาปูชิโนร้อน') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 45 FROM menu_items WHERE name='คาปูชิโน' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('คาปูชิโน เย็น', 'คาปูชิโนเย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 50 FROM menu_items WHERE name='คาปูชิโน' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('คาปูชิโน ปั่น', 'คาปูชิโนปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'ชานม', 35, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ร้อน', 35 FROM menu_items WHERE name='ชานม' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ชานม ร้อน', 'ชานมร้อน') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 35 FROM menu_items WHERE name='ชานม' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ชานม เย็น', 'ชานมเย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 40 FROM menu_items WHERE name='ชานม' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ชานม ปั่น', 'ชานมปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'ชาเขียว', 35, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ร้อน', 35 FROM menu_items WHERE name='ชาเขียว' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ชาเขียว ร้อน', 'ชาเขียวร้อน') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 35 FROM menu_items WHERE name='ชาเขียว' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ชาเขียว เย็น', 'ชาเขียวเย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 40 FROM menu_items WHERE name='ชาเขียว' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ชาเขียว ปั่น', 'ชาเขียวปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'โกโก้', 35, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ร้อน', 35 FROM menu_items WHERE name='โกโก้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('โกโก้ ร้อน', 'โกโก้ร้อน') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 35 FROM menu_items WHERE name='โกโก้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('โกโก้ เย็น', 'โกโก้เย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 40 FROM menu_items WHERE name='โกโก้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('โกโก้ ปั่น', 'โกโก้ปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'ช็อกโกแลตลาเต้', 45, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'เย็น', 45 FROM menu_items WHERE name='ช็อกโกแลตลาเต้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ช็อกโกแลตลาเต้ เย็น', 'ช็อกโกแลตลาเต้เย็น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 50 FROM menu_items WHERE name='ช็อกโกแลตลาเต้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('ช็อกโกแลตลาเต้ ปั่น', 'ช็อกโกแลตลาเต้ปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

INSERT INTO menu_items(shop_id,name,price,is_available)
SELECT shop_id, 'นมสดโอริโอ้', 40, 1 FROM shops WHERE shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price, is_available=1;

INSERT INTO menu_variants(menu_id,name,price)
SELECT menu_id, 'ปั่น', 40 FROM menu_items WHERE name='นมสดโอริโอ้' AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์')
ON CONFLICT(menu_id,name) DO UPDATE SET price=excluded.price;

UPDATE menu_items SET is_available=0 WHERE name IN ('นมสดโอริโอ้ ปั่น', 'นมสดโอริโอ้ปั่น') AND shop_id IN (SELECT shop_id FROM shops JOIN canteens USING(canteen_id) WHERE shops.name = 'ร้านพี่ฝน' AND canteens.name = 'คณะครุศาสตร์');

-- These four items have explicit prices on the sign. No unknown dish prices are guessed.
UPDATE menu_items SET is_available=1
WHERE name IN ('หมูยอ','กุนเชียง','ไข่ดาว','ไข่เจียว')
AND shop_id IN (
    SELECT shop_id FROM shops JOIN canteens USING(canteen_id)
    WHERE shops.name='ร้านพี่ชายข้าวราดแกง' AND canteens.name='คณะครุศาสตร์'
);
RELEASE SAVEPOINT drink_variants;
