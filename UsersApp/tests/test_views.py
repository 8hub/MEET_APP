import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from UsersApp.views import index
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersAppViewTest(TestCase):
    def test_index_view(self):
        index_page = HttpResponseRedirect(reverse("UsersApp:index"))
        self.assertEqual(index_page.url, "/users/")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("UsersApp:index"))
        self.assertEqual(response.status_code, 200)


    def test_login_view_template(self):
        response = self.client.get(reverse("UsersApp:login"))
        self.assertTemplateUsed(response, "UsersApp/login.html")
    
    def test_login_view_redirect(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(reverse("UsersApp:login"), {"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 302)
        
    def test_fail(self):
        self.assertEqual(1+1, 3)