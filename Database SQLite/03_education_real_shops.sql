-- Approved photo transcription for the Education canteen.

-- Run 02_shop_visibility.sql once on existing databases before this file.

PRAGMA foreign_keys = ON;

SAVEPOINT education_real_shops;

INSERT INTO canteens(name) VALUES ('คณะครุศาสตร์') ON CONFLICT(name) DO NOTHING;

INSERT INTO shops(canteen_id,name,shop_type,is_active) SELECT canteen_id,'ร้านครัวสิริ','regular',1 FROM canteens WHERE name='คณะครุศาสตร์' ON CONFLICT(canteen_id,name) DO UPDATE SET is_active=1;

INSERT INTO shops(canteen_id,name,shop_type,is_active) SELECT canteen_id,'ร้านแม่อุ่นเรือน','regular',1 FROM canteens WHERE name='คณะครุศาสตร์' ON CONFLICT(canteen_id,name) DO UPDATE SET is_active=1;

INSERT INTO shops(canteen_id,name,shop_type,is_active) SELECT canteen_id,'ร้านพี่ฝน','regular',1 FROM canteens WHERE name='คณะครุศาสตร์' ON CONFLICT(canteen_id,name) DO UPDATE SET is_active=1;

INSERT INTO shops(canteen_id,name,shop_type,is_active) SELECT canteen_id,'ร้านพี่ชายข้าวราดแกง','curry',1 FROM canteens WHERE name='คณะครุศาสตร์' ON CONFLICT(canteen_id,name) DO UPDATE SET is_active=1;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ก๋วยเตี๋ยวหมูต้มยำ',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ก๋วยเตี๋ยวหมูน้ำใส',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ก๋วยเตี๋ยวหมูน้ำข้น',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ก๋วยเตี๋ยวเย็นตาโฟ',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'บะหมี่–เกี๊ยว หมูแดง',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'บะหมี่–เกี๊ยว ไก่แซ่บ',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวขาหมู',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวหมูแดง',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวหมูกรอบ',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวไก่แดง',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวมันไก่ต้ม',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวมันไก่ทอด',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวมันไก่ย่าง',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ผัดซีอิ๊ว',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ราดหน้า',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'สุกี้น้ำ',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'สุกี้แห้ง',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'มาม่าผัดขี้เมา',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ส้มตำไทย',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ส้มตำปูปลาร้า',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ตำแตง',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ตำถั่ว',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ลาบหมู',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ลาบไก่',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ต้มยำหมูชิ้น',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ต้มยำไก่',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ต้มยำทะเล',60,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ขนมจีนน้ำยากะทิ',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ขนมจีนป่าไก่โคราช',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ข้าวสวย',10,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ขนมจีนเปล่า',10,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ยำอกไก่',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านแม่อุ่นเรือน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'เอสเพรสโซ่ร้อน',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'เอสเพรสโซ่เย็น',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'เอสเพรสโซ่ปั่น',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ลาเต้ร้อน',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ลาเต้เย็น',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ลาเต้ปั่น',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'คาปูชิโนร้อน',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'คาปูชิโนเย็น',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'คาปูชิโนปั่น',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ชานมร้อน',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ชานมเย็น',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ชานมปั่น',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ชาเขียวร้อน',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ชาเขียวเย็น',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ชาเขียวปั่น',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'โกโก้ร้อน',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'โกโก้เย็น',35,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'โกโก้ปั่น',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ช็อกโกแลตลาเต้เย็น',45,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ช็อกโกแลตลาเต้ปั่น',50,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'นมสดโอริโอ้ปั่น',40,1,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ฝน' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type,dish_count) SELECT shop_id,'ข้าวราดแกง 1 อย่าง',30,1,'curry_price',1 FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type,dish_count) SELECT shop_id,'ข้าวราดแกง 2 อย่าง',40,1,'curry_price',2 FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type,dish_count) SELECT shop_id,'ข้าวราดแกง 3 อย่าง',45,1,'curry_price',3 FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'กับข้าวเป็นถ้วย',20,0,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'หมูยอ',10,0,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'กุนเชียง',10,0,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ไข่ดาว',10,0,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_items(shop_id,name,price,is_available,menu_type) SELECT shop_id,'ไข่เจียว',10,0,'regular' FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านพี่ชายข้าวราดแกง' ON CONFLICT(shop_id,name) DO UPDATE SET price=excluded.price;

INSERT INTO menu_options(shop_id,group_name,name,extra_price) SELECT shop_id,'ขนาด','ธรรมดา',0 FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,group_name,name) DO UPDATE SET extra_price=excluded.extra_price;

INSERT INTO menu_options(shop_id,group_name,name,extra_price) SELECT shop_id,'ขนาด','พิเศษ',10 FROM shops JOIN canteens USING(canteen_id) WHERE canteens.name='คณะครุศาสตร์' AND shops.name='ร้านครัวสิริ' ON CONFLICT(shop_id,group_name,name) DO UPDATE SET extra_price=excluded.extra_price;

UPDATE shops SET is_active=0 WHERE canteen_id=(SELECT canteen_id FROM canteens WHERE name='คณะครุศาสตร์') AND name IN ('ร้านข้าวแกง','ร้านก๋วยเตี๋ยว','ร้านน้ำผลไม้');

RELEASE SAVEPOINT education_real_shops;
