import unittest
from pathlib import Path

from Backend import catalog, menu
import test_catalog


class DrinkVariantTests(unittest.TestCase):
    setUp = test_catalog.CatalogTests.setUp
    tearDown = test_catalog.CatalogTests.tearDown

    def load_real_menus(self):
        folder = Path(__file__).resolve().parent.parent / 'Database SQLite'
        for filename in ('03_education_real_shops.sql', '04_drink_variants.sql'):
            self.connection.executescript((folder / filename).read_text(encoding='utf-8'))

    def test_drink_choices_prices_and_old_menu_hidden(self):
        self.load_real_menus()
        data = catalog.get_menu_data('คณะครุศาสตร์', 'ร้านพี่ฝน')
        self.assertEqual(len(data[1]['ร้านพี่ฝน']), 8)
        self.assertEqual(data[3]['ช็อกโกแลตลาเต้'], {'เย็น': 45, 'ปั่น': 50})
        self.assertEqual(data[3]['นมสดโอริโอ้'], {'ปั่น': 40})
        for name, choices in data[3].items():
            for kind, price in choices.items():
                item = dict(canteen='คณะครุศาสตร์', shop='ร้านพี่ฝน', menu=name,
                            price=price, options=[f'รูปแบบ: {kind}'])
                catalog.check_cart_item(item)
        item = dict(canteen='คณะครุศาสตร์', shop='ร้านพี่ฝน', menu='นมสดโอริโอ้',
                    price=40, options=['รูปแบบ: ร้อน'])
        with self.assertRaises(ValueError):
            catalog.check_cart_item(item)
        item['options'] = []
        with self.assertRaises(ValueError):
            catalog.check_cart_item(item)
        item['options'] = ['รูปแบบ: ปั่น']
        self.connection.execute("UPDATE menu_variants SET price=41 WHERE menu_id IN (SELECT menu_id FROM menu_items WHERE name='นมสดโอริโอ้')")
        self.connection.commit()
        with self.assertRaises(ValueError):
            catalog.check_cart_item(item)
        self.connection.execute("UPDATE menu_variants SET is_available=0 WHERE menu_id IN (SELECT menu_id FROM menu_items WHERE name='นมสดโอริโอ้')")
        self.connection.commit()
        self.assertNotIn('นมสดโอริโอ้', catalog.get_menu_data('คณะครุศาสตร์', 'ร้านพี่ฝน')[1]['ร้านพี่ฝน'])

    def test_regular_item_in_curry_shop(self):
        self.load_real_menus()
        item = dict(canteen='คณะครุศาสตร์', shop='ร้านพี่ชายข้าวราดแกง',
                    menu='ไข่ดาว', price=10, options=[])
        catalog.check_cart_item(item)
        data = catalog.get_menu_data(item['canteen'], item['shop'])
        self.assertEqual(menu.calculate_price(item['shop'], 'ไข่ดาว', menu_data=data), 10)
        self.assertEqual(data[0][item['shop']]['prices'], {1: 30, 2: 40, 3: 45})

    def test_noodle_options_do_not_leak_into_rice(self):
        self.load_real_menus()
        path = Path(__file__).resolve().parent.parent / 'Database SQLite' / '06_noodle_options.sql'
        self.connection.executescript(path.read_text(encoding='utf-8'))
        data = catalog.get_menu_data('คณะครุศาสตร์', 'ร้านครัวสิริ')
        groups = menu.get_option_groups('ร้านครัวสิริ', 'ก๋วยเตี๋ยวหมูต้มยำ', data)
        self.assertEqual(set(groups['เส้น']), {'เส้นเล็ก','เส้นใหญ่','เส้นหมี่','บะหมี่'})
        self.assertNotIn('เส้น', menu.get_option_groups('ร้านครัวสิริ','ข้าวขาหมู',data))
        item = dict(canteen='คณะครุศาสตร์',shop='ร้านครัวสิริ',menu='ก๋วยเตี๋ยวหมูต้มยำ',
                    price=60,options=['เส้น: เส้นเล็ก','รูปแบบ: แห้ง','ขนาด: พิเศษ'])
        catalog.check_cart_item(item)
        item['options'] = ['รูปแบบ: แห้ง','ขนาด: พิเศษ']
        with self.assertRaises(ValueError):
            catalog.check_cart_item(item)
