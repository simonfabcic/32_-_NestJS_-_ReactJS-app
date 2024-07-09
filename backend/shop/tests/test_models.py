from django.db import IntegrityError
from django.test import TestCase
from shop.factory import ProductFactory, ShopProfileFactory
from shop.models import Order, OrderItem


class OrderModelTests(TestCase):
    def setUp(self):
        self.product1 = ProductFactory()
        self.product2 = ProductFactory()
        self.shopProfile = ShopProfileFactory()
        self.order = Order.objects.create(buyer=self.shopProfile)

    def test_unique_order_product_constraint(self):
        OrderItem.objects.create(order=self.order, product=self.product1, quantity=2)

        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                order=self.order, product=self.product1, quantity=1
            )

    def test_order_total_quantity(self):
        OrderItem.objects.create(order=self.order, product=self.product1, quantity=2)
        OrderItem.objects.create(order=self.order, product=self.product2, quantity=3)

        order_items = OrderItem.objects.filter(order=self.order)
        total_quantity = sum(item.quantity for item in order_items)

        self.assertEqual(total_quantity, 5)

    def test_product_removal_from_order(self):
        order_item = OrderItem.objects.create(
            order=self.order, product=self.product1, quantity=2
        )

        order_items = OrderItem.objects.filter(order=self.order)
        self.assertEqual(order_items.count(), 1)

        order_item.delete()
        self.assertEqual(OrderItem.objects.count(), 0)

        order_items = OrderItem.objects.filter(order=self.order)
        self.assertEqual(order_items.count(), 0)

    def test_multiple_orders(self):
        order2 = Order.objects.create(buyer=self.shopProfile)
        OrderItem.objects.create(order=self.order, product=self.product1, quantity=2)
        OrderItem.objects.create(order=order2, product=self.product1, quantity=1)

        self.assertEqual(OrderItem.objects.filter(order=self.order).count(), 1)
        self.assertEqual(OrderItem.objects.filter(order=order2).count(), 1)
        # orders are different
        self.assertNotEqual(OrderItem.objects.get(order=self.order).order, order2)
