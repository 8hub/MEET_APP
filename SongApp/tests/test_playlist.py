import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from SongApp.models import Song, Playlist

class PlaylistViewSetTestCase(APITestCase):
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

### REQUESTS working WITH AUTHENTICATION ###
    def test_create_playlist(self):
        url = reverse('SongApp:playlist-list')
        data = {'title': 'New Playlist'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_playlist(self):
        url = reverse('SongApp:playlist-detail', kwargs={'pk': self.playlist.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_playlist(self):
        url = reverse('SongApp:playlist-detail', kwargs={'pk': self.playlist.pk})
        response = self.client.put(url, {'title': 'New Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'New Title')

    def test_add_songs_to_playlist(self):
        url = reverse('SongApp:playlist-add-songs', kwargs={'pk': self.playlist.pk})
        response = self.client.post(url, {'song_ids': [self.song.pk]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.playlist.songs.count(), 1)
        self.assertEqual(response.data[0]['title'], 'Sample Song')

    def test_remove_songs_from_playlist(self):
        self.playlist.songs.add(self.song)
        self.assertEqual(self.playlist.songs.count(), 1)
        url = reverse('SongApp:playlist-remove-songs', kwargs={'pk': self.playlist.pk})
        response = self.client.post(url, {'song_ids': [self.song.pk]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.playlist.songs.count(), 0)

    def test_update_playlist_title(self):
        url = reverse('SongApp:playlist-update-title', kwargs={'pk': self.playlist.pk})
        response = self.client.put(url, {'title': 'New Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'New Title')
        
class PlaylistNoAuthenticationViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()

    def setUp(self):
        self.user = self.User.objects.create_user(username='user', email="email@user.com", password='P4$1ddfc77')
        self.user2 = self.User.objects.create_user(username='user2', email="email2@user.com", password='paDsf$#5134')
        
        self.song = Song.objects.create(title='Sample Song', artist='Artist', url_field="http://testmp3.com", added_by=self.user)
        self.song2 = Song.objects.create(title='Sample Song 2', artist='Artist2', url_field="http://testmp3.com", added_by=self.user2)
        self.playlist = Playlist.objects.create(title='Sample Playlist', created_by=self.user)

### REQUESTS working WITHOUT AUTHENTICATION ###
    def test_get_playlists(self):
        url = reverse('SongApp:playlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_playlist(self):
        url = reverse('SongApp:playlist-detail', kwargs={'pk': self.playlist.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_songs(self):
        url = reverse('SongApp:playlist-get-songs', kwargs={'pk': self.playlist.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

### REQUESTS NOT working WITHOUT AUTHENTICATION ###
    def test_create_playlist(self):
        url = reverse('SongApp:playlist-list')
        data = {'title': 'New Playlist'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_playlist(self):
        url = reverse('SongApp:playlist-detail', kwargs={'pk': self.playlist.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_playlist(self):
        url = reverse('SongApp:playlist-detail', kwargs={'pk': self.playlist.pk})
        response = self.client.put(url, {'title': 'New Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
       
    def test_add_songs_to_playlist(self):
        url = reverse('SongApp:playlist-add-songs', kwargs={'pk': self.playlist.pk})
        response = self.client.post(url, {'song_ids': [self.song.pk]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_remove_songs_from_playlist(self):
        url = reverse('SongApp:playlist-remove-songs', kwargs={'pk': self.playlist.pk})
        response = self.client.post(url, {'song_ids': [self.song.pk]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_playlist_title(self):
        url = reverse('SongApp:playlist-update-title', kwargs={'pk': self.playlist.pk})
        response = self.client.put(url, {'title': 'New Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)