import unittest
import test_system_review
import test_catalog
from Backend import orders, order_history, shop_orders, users


class OrderCancellationTests(unittest.TestCase):
    setUp = test_catalog.CatalogTests.setUp
    tearDown = test_catalog.CatalogTests.tearDown
    make_order = test_system_review.SystemReviewTests.make_order

    def test_cancel_keeps_history_and_blocks_shop_confirmation(self):
        order_id = self.make_order()
        orders.cancel_order(order_id)
        order, items = order_history.read_details(order_id)
        self.assertEqual(order['status'], 'cancelled')
        self.assertEqual(len(items), 1)
        with self.assertRaises(ValueError):
            orders.cancel_order(order_id)
        users.create_account('seller', 'password123', 'Seller', 'shop', 3)
        self.connection.execute("UPDATE users SET is_approved=1 WHERE role='shop'")
        self.connection.commit()
        users.login('seller', 'password123')
        with self.assertRaises(ValueError):
            shop_orders.change_status(order_id, 'คณะครุศาสตร์', 'ร้านน้ำผลไม้',
                                      'awaiting_payment_review', 'paid')

    def test_only_waiting_status_can_be_cancelled(self):
        order_id = self.make_order()
        for status in ['pending', 'payment_rejected', 'paid', 'preparing', 'ready', 'completed']:
            with self.subTest(status=status):
                self.connection.execute('UPDATE orders SET status=? WHERE order_id=?', (status, order_id))
                self.connection.commit()
                with self.assertRaises(ValueError):
                    orders.cancel_order(order_id)
                self.assertEqual(order_history.read_details(order_id)[0]['status'], status)

    def test_other_customer_cannot_cancel(self):
        order_id = self.make_order()
        users.register_customer('other', 'password123', 'Other')
        users.login('other', 'password123')
        with self.assertRaises(ValueError):
            orders.cancel_order(order_id)
        self.assertEqual(self.connection.execute('SELECT status FROM orders WHERE order_id=?',
                                               (order_id,)).fetchone()[0], 'awaiting_payment_review')

    def test_shop_confirmation_first_blocks_customer_cancellation(self):
        order_id = self.make_order()
        users.create_account('seller', 'password123', 'Seller', 'shop', 3)
        self.connection.execute("UPDATE users SET is_approved=1 WHERE role='shop'")
        self.connection.commit()
        users.login('seller', 'password123')
        shop_orders.change_status(order_id, 'คณะครุศาสตร์', 'ร้านน้ำผลไม้', 'awaiting_payment_review', 'paid')
        users.login('tester', 'password123')
        with self.assertRaises(ValueError):
            orders.cancel_order(order_id)
        self.assertEqual(order_history.read_details(order_id)[0]['status'], 'paid')
