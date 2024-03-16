from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Playlist, Song, PlaylistSong
from .forms import AddSongForm, AddPlaylistForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

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
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        song_id = request.POST.get("song_id")
        try:
            song = Song.objects.get(pk=song_id)
            PlaylistSong.objects.create(playlist=playlist, song=song)
            messages.success(request, "Song added to playlist successfully")
            return HttpResponseRedirect(reverse("SongRequests:playlist", args=(playlist_id,)))
        except Song.DoesNotExist:
            messages.error(request, "Song does not exist")
            return HttpResponseRedirect(reverse("SongRequests:playlist", args=(playlist_id,)))
        except Exception as e:
            messages.error(request, f"An error occured: {str(e)}")
            return HttpResponseRedirect(reverse("SongRequests:playlist", args=(playlist_id,)))
    return HttpResponseRedirect(reverse("SongRequests:index"))


@login_required(login_url="../users/login")
def add_playlist(request):
    form = AddPlaylistForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        anonymous = form.cleaned_data["anonymous"]
        new_playlist = Playlist.objects.create(
            title=title, anonymous=anonymous, created_by=request.user)

        selected_songs_ids = form.cleaned_data["songs"]
        try:
            new_playlist.add_songs(selected_songs_ids)
            messages.success(request, "Playlist created successfully")
            return HttpResponseRedirect(reverse("SongRequests:index"))
        except ObjectDoesNotExist as e:
            messages.error(request, f"An error occured: {str(e)}")
            new_playlist.delete()

    return render(request, "SongRequests/add_playlist.html",{
            "form":form
    })
