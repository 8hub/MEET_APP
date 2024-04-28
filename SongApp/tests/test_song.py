from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from SongApp.models import Song, Playlist


class SongViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()
    def setUp(self):
        # Create a user
        self.user = self.User.objects.create_user(username='user', email="email@user.com", password='P4$1ddfc77')
        self.user2 = self.User.objects.create_user(username='user2', email="email2@user.com", password='paDsf$#5134')
        
        # Create songs and playlists (self.user is the creator)
        self.song = Song.objects.create(title='Sample Song', artist='Artist', url_field="http://testmp3.com", added_by=self.user)
        self.playlist = Playlist.objects.create(title='Sample Playlist', created_by=self.user)

        # Get token for auth
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        
    def test_create_song(self):
        url = reverse('SongApp:song-list')
        data = {'title': 'New Song', 'artist': 'New Artist', 'url_field': 'http://newsong.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 2)

    def test_update_song(self):
        url = reverse('SongApp:song-detail', kwargs={'pk': self.song.pk})
        new_title = 'New Title'
        response = self.client.put(url, {'title': new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, new_title)

    def test_delete_song(self):
        url = reverse('SongApp:song-detail', kwargs={'pk': self.song.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Song.objects.count(), 0)
    
    def test_add_song_to_playlist(self):
        url = reverse('SongApp:song-add-to-playlist', kwargs={'pk': self.song.pk})
        response = self.client.post(url, {'playlist_id': self.playlist.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.song, self.playlist.songs.all())

    def test_remove_song_from_playlist(self):
        self.playlist.songs.add(self.song)
        url = reverse('SongApp:song-remove-from-playlist', kwargs={'pk': self.song.pk})
        response = self.client.post(url, {'playlist_id': self.playlist.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.song, self.playlist.songs.all())

    def test_update_artist_no_permission(self):
        # Test with user who is not the creator
        self.token = RefreshToken.for_user(self.user2).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse('SongApp:song-update-artist', kwargs={'pk': self.song.pk})
        response = self.client.put(url, {'artist': 'New Artist'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_artist(self):
        url = reverse('SongApp:song-update-artist', kwargs={'pk': self.song.pk})
        new_artist = 'New Artist'
        response = self.client.put(url, {'artist': new_artist}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.artist, new_artist)

    def test_update_title(self):
        url = reverse('SongApp:song-update-title', kwargs={'pk': self.song.pk})
        new_title = 'New fresh Title'
        response = self.client.put(url, {'title': new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, new_title)

    def test_update_title_no_permission(self):
        # Test with user who is not the creator
        self.token = RefreshToken.for_user(self.user2).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse('SongApp:song-update-title', kwargs={'pk': self.song.pk})
        response = self.client.put(url, {'title': 'New fresh Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_url(self):
        url = reverse('SongApp:song-update-url', kwargs={'pk': self.song.pk})
        new_url = 'http://newurl.com'
        response = self.client.put(url, {'url_field': new_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.url_field, new_url)

    def test_update_url_no_permission(self):
        # Test with user who is not the creator
        self.token = RefreshToken.for_user(self.user2).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse('SongApp:song-update-url', kwargs={'pk': self.song.pk})
        response = self.client.put(url, {'url_field': 'http://newurl.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class SongViewSetNoAuthenticationTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()

    def setUp(self):
        self.user = self.User.objects.create_user(username='user', email="email@user.com", password='P4$1ddfc77')
        self.user2 = self.User.objects.create_user(username='user2', email="email2@user.com", password='paDsf$#5134')
        
        self.song = Song.objects.create(title='Sample Song', artist='Artist', url_field="http://testmp3.com", added_by=self.user)
        self.playlist = Playlist.objects.create(title='Sample Playlist', created_by=self.user)
        
        self.client.credentials()
        
    def test_get_song(self):
        url = reverse('SongApp:song-detail', kwargs={'pk': self.song.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_songs(self):
        url = reverse('SongApp:song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_playlists(self):
        self.playlist.songs.add(self.song)
        url = reverse('SongApp:song-get-playlists', kwargs={'pk': self.song.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_song_unauthorized(self):
        url = reverse('SongApp:song-list')
        data = {'title': 'New Song', 'artist': 'New Artist', 'url_field': 'http://newsong.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Song.objects.count(), 1)

    def test_delete_song_unauthorized(self):
        url = reverse('SongApp:song-detail', kwargs={'pk': self.song.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Song.objects.count(), 1)
    
    def test_add_to_playlist_unauthorized(self):
        url = reverse('SongApp:song-add-to-playlist', kwargs={'pk': self.song.pk})
        response = self.client.post(url, {'playlist_id': self.playlist.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn(self.song, self.playlist.songs.all())

    def test_remove_from_playlist_unauthorized(self):
        self.playlist.songs.add(self.song)
        url = reverse('SongApp:song-remove-from-playlist', kwargs={'pk': self.song.pk})
        response = self.client.post(url, {'playlist_id': self.playlist.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(self.song, self.playlist.songs.all())

    def test_update_artist_unauthorized(self):
        url = reverse('SongApp:song-update-artist', kwargs={'pk': self.song.pk})
        response = self.client.put(url, {'artist': 'New Artist'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.song.refresh_from_db()
        self.assertNotEqual(self.song.artist, 'New Artist')

    def test_update_title_unauthorized(self):
        url = reverse('SongApp:song-update-title', kwargs={'pk': self.song.pk})
        response = self.client.put(url, {'title': 'New fresh Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.song.refresh_from_db()
        self.assertNotEqual(self.song.title, 'New fresh Title')
    
    def test_update_url_unauthorized(self):
        url = reverse('SongApp:song-update-url', kwargs={'pk': self.song.pk})
        response = self.client.put(url, {'url_field': 'http://newurl.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.song.refresh_from_db()
        self.assertNotEqual(self.song.url_field, 'http://newurl.com')