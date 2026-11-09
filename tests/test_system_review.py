import unittest
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock

import test_catalog
from Backend import cart, catalog, checkout, orders, shop_orders, users
from Frontend.auto_refresh_frame import AutoRefreshFrame


class SystemReviewTests(unittest.TestCase):
    setUp = test_catalog.CatalogTests.setUp
    tearDown = test_catalog.CatalogTests.tearDown

    def make_order(self):
        item = dict(canteen='คณะครุศาสตร์',shop='ร้านน้ำผลไม้',menu='น้ำส้ม',
                    price=25,quantity=1,options=[],note='')
        date = (datetime.now(checkout.THAI_TIME)+timedelta(days=1)).date().isoformat()
        return orders.save_order(item['canteen'],item['shop'],[item],'Test','0812345678',date,'12:00')

    def test_rename_keeps_history_and_status_permissions(self):
        oid = self.make_order()
        users.create_account('seller','password123','Seller','shop',3)
        users.login('seller','password123')
        self.connection.execute("UPDATE shops SET name='New shop name' WHERE shop_id=3")
        self.connection.commit()
        rows = shop_orders.read_orders('คณะครุศาสตร์','New shop name')
        self.assertEqual(rows[0]['order_id'],oid)
        self.assertEqual(rows[0]['shop_name'],'ร้านน้ำผลไม้')
        self.assertEqual(len(shop_orders.read_items(oid,'คณะครุศาสตร์','New shop name')),1)
        with self.assertRaises(ValueError):
            shop_orders.change_status(oid,'คณะครุศาสตร์','New shop name','awaiting_payment_review','ready')
        statuses=['awaiting_payment_review','payment_rejected','awaiting_payment_review','paid','preparing','ready','completed']
        for old,new in zip(statuses,statuses[1:]):
            shop_orders.change_status(oid,'คณะครุศาสตร์','New shop name',old,new)
        with self.assertRaises(ValueError):
            shop_orders.change_status(oid,'คณะครุศาสตร์','New shop name','ready','completed')

    def test_cart_keeps_different_variants_and_shops_separate(self):
        items=[]
        for kind in ['ร้อน','เย็น','เย็น']:
            cart.add_item(items,'A','Drink','Tea',35,[f'รูปแบบ: {kind}'])
        cart.add_item(items,'B','Drink','Tea',35,['รูปแบบ: เย็น'])
        self.assertEqual(len(items),3)
        self.assertEqual(cart.get_total_quantity(items),4)
        self.assertEqual(cart.get_total_price(items),140)
        self.assertEqual(len(cart.get_shops(items)),2)
        cart.decrease_quantity(items[0])
        self.assertEqual(items[0]['quantity'],1)
        cart.remove_item(items,items[0])
        self.assertEqual(cart.get_total_price(items),105)

    def test_invalid_quantity_and_empty_cart(self):
        with self.assertRaises(ValueError):
            orders.check_items('A','B',[])
        for quantity in [0,-1,1.5,True]:
            with self.assertRaises(ValueError):
                orders.check_items('A','B',[dict(canteen='A',shop='B',quantity=quantity,price=10)])

    def test_pickup_and_phone_validation(self):
        now=datetime(2026,11,9,12,0,tzinfo=checkout.THAI_TIME)
        for date,time in [('2026-11-09','11:59'),('2026-11-09','12:00'),('2026-02-30','12:00')]:
            self.assertTrue(checkout.check_pickup_time(date,time,now))
        self.assertEqual(checkout.check_pickup_time('2026-11-09','12:01',now),'')
        for phone in ['','08123','1812345678','081abc5678','๐๘๑๒๓๔๕๖๗๘']:
            self.assertTrue(checkout.check_phone(phone))
        self.assertEqual(checkout.check_phone('0812345678'),'')

    def test_polling_retries_after_failed_read(self):
        frame=SimpleNamespace(refresh_paused=False,read_version=Mock(return_value=2),
            data_version=1,refresh_page=Mock(side_effect=[False,None]),
            after=Mock(return_value='timer'),check_for_updates=Mock(),refresh_timer=None)
        AutoRefreshFrame.check_for_updates(frame)
        self.assertEqual(frame.data_version,1)
        AutoRefreshFrame.check_for_updates(frame)
        self.assertEqual(frame.data_version,2)
        AutoRefreshFrame.check_for_updates(frame)
        self.assertEqual(frame.refresh_page.call_count,2)
