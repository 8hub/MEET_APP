from django.db import models
from django.conf import settings



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
    

class Playlist(models.Model):
    name = models.CharField(max_length=64)
    songs = models.ManyToManyField(Song, blank=True, related_name="parent_playlists")
    anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="playlists")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} playlist"
    
    def count(self):
        return self.songs.count()
