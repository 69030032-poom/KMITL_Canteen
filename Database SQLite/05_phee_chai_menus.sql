-- Prices copied from the existing made-to-order shop, as requested.
-- These are provisional prices, not verified prices from the real shop's sign.
PRAGMA foreign_keys = ON;
SAVEPOINT phee_chai_menus;
INSERT INTO menu_items(shop_id, name, price, is_available, menu_type)
SELECT shop_id, 'ข้าวกะเพรา', 50, 1, 'regular'
FROM shops JOIN canteens USING(canteen_id)
WHERE shops.name='ร้านพี่ชายข้าวราดแกง' AND canteens.name='คณะครุศาสตร์'
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id, name, price, is_available, menu_type)
SELECT shop_id, 'ข้าวผัด', 45, 1, 'regular'
FROM shops JOIN canteens USING(canteen_id)
WHERE shops.name='ร้านพี่ชายข้าวราดแกง' AND canteens.name='คณะครุศาสตร์'
ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;
RELEASE SAVEPOINT phee_chai_menus;
