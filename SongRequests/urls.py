from django.urls import path
from . import views

app_name = "SongRequests"
urlpatterns = [
    path("", views.index, name="index"),
    path("add_song", views.add_song, name="add_song"),
    path("add_playlist", views.add_playlist, name="add_playlist"),
    path("playlist/<int:playlist_id>", views.playlist, name="playlist"),
    path("playlist/<int:playlist_id>/add_song", views.add_song_to_playlist, name="add_song_to_playlist"),
]
