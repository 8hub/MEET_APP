from django.test import TestCase
from UsersApp.models import User
from django.core.exceptions import ValidationError

class UserTest(TestCase):
    def test_model_with_correct_data(self):
        self.assertEqual(User.objects.count(), 0)
        User.objects.create_user(username="testuser", email="test@email.com", password="testpassword")
        self.assertEqual(User.objects.count(), 1)
    
    def test_model_with_incorrect_data(self):
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ValidationError):
            User.objects.create_user(username="testuser", email="testemail.com", password="testuser")
        self.assertEqual(User.objects.count(), 0)