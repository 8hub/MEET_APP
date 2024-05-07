from django.db import IntegrityError, models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist



class Song(models.Model):
    title = models.CharField(max_length=64)
    artist = models.CharField(max_length=64, blank=True, null=True)
    url_field = models.URLField(max_length=200, blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="songs")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} by {self.artist}"
    
    def __repr__(self):
        return f"{self.title} by {self.artist}"
    
    def save(self, *args, **kwargs):
        if self.title:
            super().save(*args, **kwargs)
        else:
            raise ValueError("Song must have a title.")
    

class Playlist(models.Model):
    title = models.CharField(max_length=64, unique=True)
    songs = models.ManyToManyField('Song', through='PlaylistSong', blank=True, related_name="parent_playlists")
    anonymous = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="playlists")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} playlist"
    
    def save(self, *args, **kwargs):
        if self.title:
            if not self.id:
                if Playlist.objects.filter(title=self.title).exists():
                    raise IntegrityError("Playlist with this title already exists.")
            else:
                if Playlist.objects.filter(title=self.title).exclude(id=self.id).exists():
                    raise IntegrityError("Another playlist with this title already exists.")
            super().save(*args, **kwargs)
        else:
            raise ValueError("Playlist must have a title.")
        
    def count(self):
        return self.songs.count()

    def list_songs_by_add_date(self):
        # 'playlistsong__add_date' refers to PlaylistSong add_date field
        return self.songs.all().order_by('playlistsong__add_date')

    def add_song(self, song_id):
        try:
            song = Song.objects.get(id=song_id)
            PlaylistSong.objects.create(playlist=self, song=song)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Song with id {song_id} does not exists")

    def add_songs(self, song_ids: list):
        for song_id in song_ids:
            self.add_song(song_id)
    
    def remove_song(self, song_id):
        try:
            PlaylistSong.objects.get(playlist=self, song_id=song_id).delete()
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Song with id {song_id} does not exists in playlist {self.title}")

    def remove_songs(self, song_ids: list):
        for song_id in song_ids:
            self.remove_song(song_id)

class PlaylistSong(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['add_date']
        unique_together = (('playlist', 'song'),)