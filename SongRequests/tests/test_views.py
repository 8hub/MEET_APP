import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from SongRequests.views import index
from django.contrib.auth import get_user_model

User = get_user_model()

class SongRequestsViewTest(TestCase):
    def test_index_view(self):
        index_page = HttpResponseRedirect(reverse("UsersApp:index"))
        self.assertEqual(index_page.url, "/users/")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("SongRequests:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse("SongRequests:index"))
        self.assertTemplateUsed(response, "SongRequests/index.html")

    def test_add_song_view_redirect_when_not_logged_in(self):
        response = self.client.get(reverse("SongRequests:add_song"))
        self.assertEqual(response.status_code, 302)
    
    def test_add_song_view_template_logged_in(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("SongRequests:add_song"))
        self.assertTemplateUsed(response, "SongRequests/add_song.html")