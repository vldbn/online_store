from django.contrib.auth.models import User
from django.test import TestCase, Client


class URLsTest(TestCase):
    """Test users URLs."""

    username = 'test_user'
    password = 'a123456789'
    signin_url = '/users/signin/'
    signup_url = '/users/signup/'
    logout_url = '/users/logout/'
    profile_url = '/users/profile/'
    update_profile_url = '/users/update/profile/'
    update_password_url = '/users/update/password/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_get_signin_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.signin_url)
        self.assertEqual(res.status_code, 302)

    def test_get_signin_page_without_auth(self):
        res = self.client.get(self.signin_url)
        self.assertEqual(res.status_code, 200)

    def test_get_signup_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.signup_url)
        self.assertEqual(res.status_code, 302)

    def test_get_signup_page_without_auth(self):
        res = self.client.get(self.signup_url)
        self.assertEqual(res.status_code, 200)

    def test_get_logout_page_without_auth(self):
        res = self.client.get(self.logout_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_profile_page_without_auth(self):
        res = self.client.get(self.profile_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_update_profile_page_without_auth(self):
        res = self.client.get(self.update_profile_url, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_update_password_page_without_auth(self):
        res = self.client.get(self.update_password_url, follow=True)
        self.assertEqual(res.status_code, 404)
