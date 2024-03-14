import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class LoggedInBaseTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="test@email.com")
        self.client.login(username="testuser", password="testpassword")
    
    def tearDown(self):
        self.client.logout()
        super().tearDown()

