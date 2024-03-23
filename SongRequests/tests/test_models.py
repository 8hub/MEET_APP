from django.db import IntegrityError
from django.test import TestCase
from SongRequests.models import Song, Playlist

class SongAddModelTest(TestCase):
    def test_model_with_correct_data(self):
        self.assertEqual(Song.objects.count(), 0)
        Song.objects.create(title="Test Song", artist="Test Artist", url_field="https://www.youtube.com/watch?v=123456")
        self.assertEqual(Song.objects.count(), 1)
    
    def test_add_song_with_no_title(self):
        self.assertEqual(Song.objects.count(), 0)
        with self.assertRaises(ValueError):
            Song.objects.create(artist="Test Artist", url_field="https://www.youtube.com/watch?v=123456")
        self.assertEqual(Song.objects.count(), 0)

    def test_add_song_with_no_artist_and_no_url(self):
        self.assertEqual(Song.objects.count(), 0)
        Song.objects.create(title="Test Song")
        self.assertEqual(Song.objects.count(), 1)
    
    def test_add_playlist(self):
        self.assertEqual(Playlist.objects.count(), 0)
        playlist = Playlist.objects.create(title="Test Playlist")
        self.assertEqual(playlist.is_anonymous(), False)
        self.assertEqual(Playlist.objects.count(), 1)

    def test_add_playlist_with_no_title(self):
        self.assertEqual(Playlist.objects.count(), 0)
        with self.assertRaises(ValueError):
            Playlist.objects.create()
        self.assertEqual(Playlist.objects.count(), 0)

    def test_add_playlist_with_same_title(self):
        self.assertEqual(Playlist.objects.count(), 0)
        Playlist.objects.create(title="Test Playlist")
        self.assertEqual(Playlist.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            Playlist.objects.create(title="Test Playlist")
        self.assertEqual(Playlist.objects.count(), 1)
    
    def test_add_song_to_existing_playlist(self):
        self.assertEqual(Song.objects.count(), 0)
        self.assertEqual(Playlist.objects.count(), 0)
        song = Song.objects.create(title="Test Song", artist="Test Artist", url_field="https://www.youtube.com/watch?v=123456")
        self.assertEqual(Song.objects.count(), 1)
        playlist = Playlist.objects.create(title="Test Playlist")
        playlist.add_songs([song.id])
        self.assertEqual(song.parent_playlists.count(), 1)
        self.assertEqual(playlist.songs.count(), 1)
        self.assertEqual(playlist.songs.first(), song)