from django.test import TestCase, Client


class URLsTest(TestCase):
    """Test cart's URLs."""

    cart_url = '/cart/'
    cart_add_url = '/cart/add/{}'

    def setUp(self):
        self.client = Client()

    def get_cart_page_without_auth(self):
        res = self.client.get(self.cart_url, follow=True)
        self.assertEqual(res.status_code, 404)
