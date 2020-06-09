from django.contrib.auth.models import User
from django.test import TestCase, Client
from orders.models import Order


class URLsTest(TestCase):
    """Test store urls."""

    create_url = '/orders/create/'
    orderlist_url = '/orders/orderlist/'
    order_detail_url = '/orders/order/{}/'

    username = 'test_user'
    password = 'test_p_123'

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        self.order = Order.objects.create(
            user=self.user
        )

    def test_get_order_create_url_without_auth(self):
        res = self.client.get(self.create_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_order_orderlist_page_without_auth(self):
        res = self.client.get(self.orderlist_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_order_order_detail_page_without_auth(self):
        res = self.client.get(self.orderlist_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_order_orderlist_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.orderlist_url)
        self.assertEqual(res.status_code, 200)
