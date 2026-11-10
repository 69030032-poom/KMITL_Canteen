import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from Backend import users, orders, catalog, checkout, scheduling, shop_management, shop_orders
import test_catalog


class HardeningTests(unittest.TestCase):
    setUp = test_catalog.CatalogTests.setUp
    tearDown = test_catalog.CatalogTests.tearDown

    def order(self, time='12:00', request_id=None):
        item=dict(canteen='คณะครุศาสตร์',shop='ร้านน้ำผลไม้',menu='น้ำส้ม',price=25,quantity=1,options=[],note='')
        date=(datetime.now(checkout.THAI_TIME)+timedelta(days=1)).date().isoformat()
        return orders.save_order(item['canteen'],item['shop'],[item],'Test','0812345678',date,time,request_id=request_id)

    def seller(self):
        uid=users.register_shop('seller','password123','Seller',3)
        self.connection.execute('UPDATE users SET is_approved=1 WHERE user_id=?',(uid,))
        self.connection.commit()
        users.login('seller','password123')
        return uid

    def test_pending_shop_and_suspension(self):
        uid=users.register_shop('seller','password123','Seller',3)
        with self.assertRaises(ValueError): users.login('seller','password123')
        self.connection.execute('UPDATE users SET is_approved=1 WHERE user_id=?',(uid,));self.connection.commit()
        users.login('seller','password123')
        self.connection.execute('UPDATE users SET is_suspended=1 WHERE user_id=?',(uid,));self.connection.commit()
        with self.assertRaises(ValueError): users.get_my_shop()

    def test_closed_shop_keeps_history_but_blocks_new_orders(self):
        self.order();self.seller()
        shop_management.save_hours('06:45','16:00',10,False)
        self.assertEqual(len(shop_orders.read_orders('คณะครุศาสตร์','ร้านน้ำผลไม้')),1)
        users.login('tester','password123')
        with self.assertRaises(ValueError): self.order()

    def test_hours_capacity_and_retry(self):
        with self.assertRaises(ValueError): self.order('03:00')
        self.connection.execute('UPDATE shops SET slot_capacity=1 WHERE shop_id=3');self.connection.commit()
        oid=self.order(request_id='request-one')
        self.assertEqual(oid,self.order(request_id='request-one'))
        with self.assertRaises(ValueError): self.order('12:05')
        with self.assertRaises(ValueError): self.order('12:15',request_id='request-one')
        self.order('12:15')
        self.assertEqual(self.connection.execute('SELECT count(*) FROM orders').fetchone()[0],2)

    def test_price_validation_uses_write_transaction(self):
        original=catalog.check_cart_item
        observed=[]
        def verify(item):
            connection=catalog._transaction_connection.get()
            self.assertTrue(connection.in_transaction)
            observed.append(True)
            original(item)
        with patch.object(catalog,'check_cart_item',verify): self.order()
        self.assertTrue(observed)
        self.connection.execute("UPDATE menu_items SET price=99 WHERE shop_id=3 AND name='น้ำส้ม'");self.connection.commit()
        with self.assertRaises(ValueError): self.order()
        self.assertEqual(self.connection.execute('SELECT count(*) FROM orders').fetchone()[0],1)

    def test_expiry_preserves_paid_orders(self):
        first=self.order();second=self.order()
        self.connection.execute("UPDATE orders SET pickup_date='2000-01-01'")
        self.connection.execute("UPDATE orders SET status='paid' WHERE order_id=?",(second,));self.connection.commit()
        scheduling.refresh_overdue()
        self.assertEqual(self.connection.execute('SELECT status FROM orders WHERE order_id=?',(first,)).fetchone()[0],'expired')
        self.assertEqual(self.connection.execute('SELECT status,is_overdue FROM orders WHERE order_id=?',(second,)).fetchone(),('paid',1))

    def test_login_lockout(self):
        for _ in range(5):
            with self.assertRaises(ValueError): users.login('tester','wrong')
        with self.assertRaisesRegex(ValueError,'5 นาที'): users.login('tester','password123')
        with patch('Backend.users.time.time',return_value=9999999999):
            users.login('tester','password123')

    def test_menu_management_and_ownership(self):
        self.seller()
        mid=shop_management.save_menu(None,'ชาใหม่',30,True,[('เย็น',35),('ปั่น',40)],[('หวาน','น้อย',0)])
        data=catalog.get_menu_data('คณะครุศาสตร์','ร้านน้ำผลไม้')
        self.assertEqual(data[3]['ชาใหม่'],{'เย็น':35,'ปั่น':40})
        with self.assertRaises(ValueError): shop_management.save_menu(1,'bad',10,True,[],[])
        shop_management.save_menu(mid,'ชาใหม่',30,False,[],[])
        self.assertNotIn('ชาใหม่',catalog.get_menu_data('คณะครุศาสตร์','ร้านน้ำผลไม้')[1]['ร้านน้ำผลไม้'])

    def test_image_upload_and_editor(self):
        import tempfile
        from PIL import Image
        from Backend import database
        from Frontend.shop_menu_page import ShopMenuPage
        import customtkinter as ctk
        self.seller()
        with tempfile.TemporaryDirectory(dir=__import__('pathlib').Path('outputs').resolve()) as folder:
            path=__import__('pathlib').Path(folder)
            Image.new('RGB',(20,20),'orange').save(path/'source.png')
            with patch.object(database,'database_file',path/'test.db'):
                mid=shop_management.save_menu(None,'ภาพทดสอบ',30,True,[],[],str(path/'source.png'))
                filename=self.connection.execute('SELECT image_path FROM menu_items WHERE menu_id=?',(mid,)).fetchone()[0]
                self.assertTrue((path/'menu_images'/filename).exists())
                root=ctk.CTk();root.withdraw()
                page=ShopMenuPage(root);page.update()
                self.assertTrue(page.winfo_exists())
                from PIL import ImageGrab
                page.geometry('960x720+20+20'); page.attributes('-topmost',True); page.deiconify(); page.lift();page.update()
                import time
                time.sleep(0.5);page.update()
                ImageGrab.grab().save('outputs/shop_menu_review.png')
                page.destroy();root.destroy()

    def test_concurrent_capacity_and_request(self):
        import tempfile, sqlite3
        from pathlib import Path
        from concurrent.futures import ThreadPoolExecutor
        from Backend import database
        with tempfile.TemporaryDirectory(dir=Path('outputs').resolve()) as folder:
            path=Path(folder)/'isolated.db'
            target=sqlite3.connect(path)
            self.connection.backup(target)
            target.execute('UPDATE shops SET slot_capacity=1 WHERE shop_id=3');target.commit();target.close()
            def connect():
                connection=sqlite3.connect(path,timeout=10)
                connection.execute('PRAGMA foreign_keys=ON')
                return connection
            def attempt(key):
                try: return self.order(request_id=key)
                except ValueError: return 'full'
            with patch.object(database,'connect_database',connect):
                with ThreadPoolExecutor(2) as pool:
                    results=list(pool.map(attempt,['same','same']))
                self.assertEqual(results[0],results[1])
                self.assertNotEqual(results[0],'full')
                with self.assertRaises(ValueError): self.order(request_id='new')
                from contextlib import closing
                with closing(connect()) as connection:
                    self.assertEqual(connection.execute('SELECT count(*) FROM orders').fetchone()[0],1)

                with closing(connect()) as connection:
                    connection.execute('DELETE FROM order_items')
                    connection.execute('DELETE FROM orders')
                    connection.commit()
                with ThreadPoolExecutor(2) as pool:
                    results=list(pool.map(attempt,['different-a','different-b']))
                self.assertEqual(results.count('full'),1)

    def test_upgrade_backups_and_preserves_rows(self):
        import tempfile, sqlite3
        from pathlib import Path
        from Backend import database
        self.order()
        with tempfile.TemporaryDirectory(dir=Path('outputs').resolve()) as folder:
            path=Path(folder)/'isolated.db'
            target=sqlite3.connect(path)
            self.connection.backup(target)
            target.execute('ALTER TABLE orders DROP COLUMN is_overdue')
            target.commit();target.close()
            with patch.object(database,'connect_database',lambda:sqlite3.connect(path)):
                database.upgrade_database()
                database.upgrade_database()
            self.assertEqual(len(list((Path(folder)/'backups').glob('*.db'))),1)
            target=sqlite3.connect(path)
            try:
                self.assertEqual(target.execute('SELECT count(*) FROM orders').fetchone()[0],1)
                self.assertIn('is_overdue',[row[1] for row in target.execute('PRAGMA table_info(orders)')])
            finally: target.close()
