from django.test import TestCase
from test_utils import LoggedInUnitBaseTest
from django.urls import reverse

class SongAppViewTest(TestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("SongApp:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse("SongApp:index"))
        self.assertTemplateUsed(response, "SongApp/index.html")

    def test_add_song_view_redirect_when_not_logged_in(self):
        response = self.client.get(reverse("SongApp:add_song"), follow=True)
        self.assertRedirects(response, "/users/login/?next=/song_request/add_song", fetch_redirect_response=False)
        self.assertTemplateUsed(response, "UsersApp/login.html")
    
class LoggedInAddSongViewTest(LoggedInUnitBaseTest):
    def test_add_song_view_status_code(self):
        response = self.client.get(reverse("SongApp:add_song"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "SongApp/add_song.html")

    def test_add_song_view_template(self):
        response = self.client.get(reverse("SongApp:add_song"))
        self.assertTemplateUsed(response, "SongApp/add_song.html")

    def test_add_song_view_post(self):
        response = self.client.post(reverse("SongApp:add_song"), {"title": "Test Song", "artist": "Test Artist", "url_field": "https://www.testurl.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("SongApp:index"))