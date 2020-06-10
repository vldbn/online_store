from django.contrib.auth.models import User
from django.test import TestCase, Client


class URLsTest(TestCase):
    """Test payments URLs."""

    username = 'test_user'
    password = 'a123456789'

    done_url = '/payments/done/'
    canceled_url = '/payments/canceled/'
    process_url = '/payments/process/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_get_process_page_without_auth(self):
        res = self.client.get(self.process_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_done_page_without_auth(self):
        res = self.client.get(self.done_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_canceled_page_without_auth(self):
        res = self.client.get(self.canceled_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_done_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.done_url)
        self.assertEqual(res.status_code, 200)

    def test_get_canceled_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.canceled_url)
        self.assertEqual(res.status_code, 200)
