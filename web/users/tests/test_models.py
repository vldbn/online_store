from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import datetime
from users.models import Profile


class ModelsTest(TestCase):
    """Test profile model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_p_123'
        )

    def test_create_profile_when_create_user(self):
        count_profiles = Profile.objects.all().count()
        self.assertEqual(count_profiles, 1)

    def test_profile_model(self):
        self.user.profile.biography = 'Some text'
        self.user.profile.address = 'Some address'
        self.user.profile.birth_date = datetime.today().day
        self.assertEqual(self.user.profile.biography, 'Some text')
        self.assertEqual(self.user.profile.address, 'Some address')
        self.assertEqual(self.user.profile.birth_date, datetime.today().day)

