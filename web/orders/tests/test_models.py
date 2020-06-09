from django.contrib.auth.models import User
from django.test import TestCase
from store.models import Product, Category
from orders.models import Order, OrderItem


class ModelsTest(TestCase):
    """Test orders models"""
    category_name = 'Test category'
    category_slug = 'test-category'

    product_name = 'Product'
    product_slug = 'product'
    product_description = 'Some text'
    product_price = 10.00

    order_item_price = 100.00

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_p_123'
        )
        self.category = Category.objects.create(
            name=self.category_name,
            slug=self.category_slug
        )

        self.product = Product.objects.create(
            category=self.category,
            name=self.product_name,
            slug=self.product_slug,
            description=self.product_description,
            price=self.product_price
        )

        self.order = Order.objects.create(
            user=self.user
        )

        self.order_item = OrderItem.objects.create(
            product=self.product,
            order=self.order,
            price=self.order_item_price
        )

    def test_order_model(self):
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(self.order.user, self.user)

    def test_order_item_model(self):
        self.assertEqual(OrderItem.objects.all().count(), 1)
        self.assertEqual(self.order_item.price, self.order_item_price)
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.order, self.order)
