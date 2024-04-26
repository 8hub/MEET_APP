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
            if self.title in Playlist.objects.values_list('title', flat=True):
                raise IntegrityError("Playlist with this title already exists.")
            super().save(*args, **kwargs)
        else:
            raise ValueError("Playlist must have a title.")
        
    def count(self):
        return self.songs.count()

    def is_anonymous(self):
        return self.anonymous

    def list_songs_by_add_date(self):
        # 'playlistsong__add_date' refers to PlaylistSong add_date field
        return self.songs.all().order_by('playlistsong__add_date')

    def add_songs(self, song_ids: list):
        try:
            for song_id in song_ids:
                song = Song.objects.get(id=song_id)
                PlaylistSong.objects.create(playlist=self, song=song)
        except ObjectDoesNotExist:
            print(f"Song with id {song_id} does not exists.")
    


class PlaylistSong(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['add_date']
        unique_together = (('playlist', 'song'),)