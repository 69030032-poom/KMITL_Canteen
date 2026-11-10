import unittest
from pathlib import Path
from datetime import datetime,timedelta
import customtkinter as ctk
import test_catalog
from Backend import users,orders,checkout
from Frontend.app import CanteenApp


class UIWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.fixture=test_catalog.CatalogTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        for name in ['03_education_real_shops.sql','04_drink_variants.sql','05_phee_chai_menus.sql','06_noodle_options.sql']:
            self.fixture.connection.executescript((Path('Database SQLite')/name).read_text(encoding='utf-8'))
        self.app=CanteenApp()
        self.addCleanup(self.app.destroy)
        self.app.geometry('1000x680+0+0')
        self.app.login_finished(users.login('tester','password123'))


    def test_customer_choices_and_fixed_action(self):
        self.app.show_menu('คณะครุศาสตร์','ร้านครัวสิริ')
        page=self.app.workspace.winfo_children()[0]
        name='ก๋วยเตี๋ยวหมูต้มยำ'
        page.show_menu_details(name)
        page.menu_choices[name]['ขนาด'].set('พิเศษ')
        page.update_regular_price(name)
        note=ctk.CTkEntry(page)
        page.add_regular_item(name,note)
        self.assertEqual(self.app.cart[0]['price'],60)
        self.assertIn('เส้น: เส้นเล็ก',self.app.cart[0]['options'])
        self.assertIn('60',page.cart_label.cget('text'))
        self.app.update()
        self.assertLessEqual(page.action_area.winfo_y()+page.action_area.winfo_height(),page.menu_panel.winfo_height())
        self.app.show_cart()
        self.app.show_menu('คณะครุศาสตร์','ร้านพี่ฝน')
        page=self.app.workspace.winfo_children()[0]
        page.show_menu_details('นมสดโอริโอ้')
        self.assertEqual(page.menu_choices['นมสดโอริโอ้']['รูปแบบ'].get(),'ปั่น')
        self.app.show_canteens()

    def test_merchant_selection_filter_and_status(self):
        item=dict(canteen='คณะครุศาสตร์',shop='ร้านครัวสิริ',menu='ข้าวขาหมู',price=50,quantity=1,options=['ขนาด: ธรรมดา'],note='')
        date=(datetime.now(checkout.THAI_TIME)+timedelta(days=1)).date().isoformat()
        oid=orders.save_order(item['canteen'],item['shop'],[item],'Preview','0812345678',date,'12:30')
        sid=self.fixture.connection.execute("SELECT shop_id FROM shops WHERE name='ร้านครัวสิริ'").fetchone()[0]
        users.create_account('previewshop','password123','Shop','shop',sid)
        self.fixture.connection.execute("UPDATE orders SET status='preparing' WHERE order_id=?",(oid,))
        self.fixture.connection.commit()
        self.app.show_login()
        self.app.login_finished(users.login('previewshop','password123'))
        page=self.app.workspace.winfo_children()[0]
        page.show_details(oid)
        page.change_filter('กำลังเตรียม')
        self.assertEqual(page.selected_order,oid)
        page.update_status(oid,'preparing','ready')
        self.assertEqual(self.fixture.connection.execute('SELECT status FROM orders WHERE order_id=?',(oid,)).fetchone()[0],'ready')
        self.assertEqual(page.selected_order,oid)
        page.change_filter('พร้อมรับ')
        self.app.update()
        self.assertLessEqual(page.actions.winfo_y()+page.actions.winfo_height(),page.detail_panel.winfo_height())
        self.app.show_login()

    def test_customer_cancel_button_and_confirmation(self):
        from unittest.mock import patch
        from Frontend.order_history_page import OrderHistoryPage
        item=dict(canteen='คณะครุศาสตร์',shop='ร้านครัวสิริ',menu='ข้าวขาหมู',price=50,quantity=1,options=['ขนาด: ธรรมดา'],note='')
        date=(datetime.now(checkout.THAI_TIME)+timedelta(days=1)).date().isoformat()
        oid=orders.save_order(item['canteen'],item['shop'],[item],'Test','0812345678',date,'12:30')
        page=OrderHistoryPage(self.app,lambda:None,oid)
        self.addCleanup(page.destroy)
        def buttons(widget):
            result=[]
            for child in widget.winfo_children():
                if isinstance(child,ctk.CTkButton):
                    result.append(child.cget('text'))
                result.extend(buttons(child))
            return result
        self.assertIn('ยกเลิกคำสั่งซื้อ',buttons(page))
        with patch('Frontend.order_history_page.messagebox.askyesno',return_value=False):
            page.cancel_order(oid)
        self.assertIn('ยกเลิกคำสั่งซื้อ',buttons(page))
        with patch('Frontend.order_history_page.messagebox.askyesno',return_value=True):
            page.cancel_order(oid)
        self.assertNotIn('ยกเลิกคำสั่งซื้อ',buttons(page))
        self.assertFalse(page.refresh_paused)
