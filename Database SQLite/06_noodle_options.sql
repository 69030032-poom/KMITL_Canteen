PRAGMA foreign_keys=ON;
SAVEPOINT noodle_options;
CREATE TABLE IF NOT EXISTS menu_item_options (
    option_id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL REFERENCES menu_items(menu_id),
    group_name TEXT NOT NULL,
    name TEXT NOT NULL,
    extra_price INTEGER NOT NULL DEFAULT 0 CHECK(extra_price >= 0),
    UNIQUE(menu_id, group_name, name)
);

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'เส้น','เส้นเล็ก',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('ก๋วยเตี๋ยวหมูต้มยำ','ก๋วยเตี๋ยวหมูน้ำใส','ก๋วยเตี๋ยวหมูน้ำข้น','ก๋วยเตี๋ยวเย็นตาโฟ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'เส้น','เส้นใหญ่',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('ก๋วยเตี๋ยวหมูต้มยำ','ก๋วยเตี๋ยวหมูน้ำใส','ก๋วยเตี๋ยวหมูน้ำข้น','ก๋วยเตี๋ยวเย็นตาโฟ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'เส้น','เส้นหมี่',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('ก๋วยเตี๋ยวหมูต้มยำ','ก๋วยเตี๋ยวหมูน้ำใส','ก๋วยเตี๋ยวหมูน้ำข้น','ก๋วยเตี๋ยวเย็นตาโฟ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'เส้น','บะหมี่',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('ก๋วยเตี๋ยวหมูต้มยำ','ก๋วยเตี๋ยวหมูน้ำใส','ก๋วยเตี๋ยวหมูน้ำข้น','ก๋วยเตี๋ยวเย็นตาโฟ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'รูปแบบ','น้ำ',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('ก๋วยเตี๋ยวหมูต้มยำ','ก๋วยเตี๋ยวหมูน้ำใส','ก๋วยเตี๋ยวหมูน้ำข้น','ก๋วยเตี๋ยวเย็นตาโฟ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'รูปแบบ','แห้ง',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('ก๋วยเตี๋ยวหมูต้มยำ','ก๋วยเตี๋ยวหมูน้ำใส','ก๋วยเตี๋ยวหมูน้ำข้น','ก๋วยเตี๋ยวเย็นตาโฟ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'รูปแบบ','น้ำ',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('บะหมี่–เกี๊ยว หมูแดง','บะหมี่–เกี๊ยว ไก่แซ่บ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;

INSERT INTO menu_item_options(menu_id,group_name,name,extra_price)
SELECT menu_id,'รูปแบบ','แห้ง',0
FROM menu_items JOIN shops USING(shop_id) JOIN canteens USING(canteen_id)
WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ'
AND menu_items.name IN ('บะหมี่–เกี๊ยว หมูแดง','บะหมี่–เกี๊ยว ไก่แซ่บ')
ON CONFLICT(menu_id,group_name,name) DO NOTHING;
RELEASE SAVEPOINT noodle_options;
