from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Playlist, Song
from django.contrib import messages

class AddSongForm(forms.Form):
    title = forms.CharField(label="Song Title", min_length=3, max_length=64)
    artist = forms.CharField(label="Artist", max_length=64, required=False)
    url_field = forms.URLField(label="URL", required=False)

def index(request):
    playlists = Playlist.objects.all()
    return render(request, "SongRequests/index.html", {
        "playlists": playlists
    })

@login_required(login_url="../users/login")
def add_song(request):
    if request.method == "POST":
        form = AddSongForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            artist = form.cleaned_data["artist"]
            url_field = form.cleaned_data["url_field"]
            song = Song(title=title, artist=artist, url_field=url_field)
            song.save()
            messages.success(request, "Song added successfully")
            return HttpResponseRedirect(reverse("SongRequests:index"))
        else:
            return render(request, "SongRequests/add_song.html",{
                "form": form
            })
    return render(request, "SongRequests/add_song.html",{
        "form": AddSongForm()
    })

def playlist(request, playlist_id):
    return render(request, "SongRequests/playlist.html",{
        "playlist": Playlist.objects.get(pk=playlist_id)
    })

def add_song_to_playlist(request, playlist_id):
    if request.method == "POST":
        playlist = Playlist.objects.get(pk=playlist_id)
        song = Song.objects.get(int(pk=request.POST["song_id"]))
        playlist.songs.add(song)
        return HttpResponseRedirect(reverse("SongRequests:playlist", args=(playlist_id,)))

def add_playlist(request):
    if request.method == "POST":
        playlist_name = request.POST["playlist_name"]
        playlist = Playlist(name=playlist_name)
        playlist.save()
