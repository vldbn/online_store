from django.contrib.auth.models import User
from django.test import TestCase, Client


class URLsTest(TestCase):
    """Test users URLs."""

    username = 'test_user'
    password = 'a123456789'
    signin = '/users/signin/'
    signup = '/users/signup/'
    logout = '/users/logout/'
    profile = '/users/profile/'
    update_profile = '/users/update/profile/'
    update_password = '/users/update/password/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_get_signin_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.signin)
        self.assertEqual(res.status_code, 302)

    def test_get_signin_page_without_auth(self):
        res = self.client.get(self.signin)
        self.assertEqual(res.status_code, 200)

    def test_get_signup_page_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get(self.signup)
        self.assertEqual(res.status_code, 302)

    def test_get_signup_page_without_auth(self):
        res = self.client.get(self.signup)
        self.assertEqual(res.status_code, 200)

    def test_get_logout_page_without_auth(self):
        res = self.client.get(self.logout, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_profile_page_without_auth(self):
        res = self.client.get(self.profile, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_update_profile_page_without_auth(self):
        res = self.client.get(self.update_profile, follow=True)
        self.assertEqual(res.status_code, 404)

    def test_get_update_password_page_without_auth(self):
        res = self.client.get(self.update_password, follow=True)
        self.assertEqual(res.status_code, 404)
