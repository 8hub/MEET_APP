from django.test import TestCase
from SongRequests.models import Song

class SongRequestLoggedInUserModelTest(TestCase):
    def test_model_with_correct_data(self):
        self.assertEqual(Song.objects.count(), 0)
        Song.objects.create(title="Test Song", artist="Test Artist", url_field="https://www.youtube.com/watch?v=123456")
        self.assertEqual(Song.objects.count(), 1)