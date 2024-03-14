from django.http import HttpResponseRedirect
from django.test import TestCase
from test_utils import LoggedInBaseTest
from django.urls import reverse
from SongRequests.views import index
from django.contrib.auth import get_user_model

User = get_user_model()

class SongRequestsViewTest(TestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("SongRequests:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse("SongRequests:index"))
        self.assertTemplateUsed(response, "SongRequests/index.html")

    def test_add_song_view_redirect_when_not_logged_in(self):
        response = self.client.get(reverse("SongRequests:add_song"), follow=True)
        self.assertRedirects(response, "/users/login/?next=/song_request/add_song", fetch_redirect_response=False)
        self.assertTemplateUsed(response, "UsersApp/login.html")
    
class LoggedInAddSongViewTest(LoggedInBaseTest):
    def test_add_song_view_status_code(self):
        response = self.client.get(reverse("SongRequests:add_song"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "SongRequests/add_song.html")
