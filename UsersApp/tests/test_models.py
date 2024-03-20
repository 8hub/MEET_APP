from django.test import TestCase
from UsersApp.models import User
from django.core.exceptions import ValidationError

class UserTest(TestCase):
    def test_model_with_correct_data(self):
        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(username="testuser", email="test@email.com", password="testpassword")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.check_password("testpassword"))
        self.assertEqual(User.objects.count(), 1)
    
    def test_model_with_invalid_password(self):
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ValidationError):
            User.objects.create_user(username="testuser", email="test@email.com", password="testuser")
        self.assertEqual(User.objects.count(), 0)

    def test_model_with_invalid_email(self):
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ValidationError):
            User.objects.create_user(username="testuser", email="testemail.com", password="testpassword")
        with self.assertRaises(ValidationError):
            User.objects.create_user(username="testuser", email="test@emailcom", password="testpassword")
        with self.assertRaises(ValidationError):
            User.objects.create_user(username="testuser", email="testemailcom", password="testpassword")
        self.assertEqual(User.objects.count(), 0)

    def test_model_with_no_username(self):
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ValueError):
            User.objects.create_user(email="test@email.com", password="testpassword")
    
    def test_model_with_no_email(self):
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ValueError):
            User.objects.create_user(username="testuser", password="testpassword")
    
    def test_model_with_no_password(self):
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ValueError):
            User.objects.create_user(username="testuser", email="test@email.com")