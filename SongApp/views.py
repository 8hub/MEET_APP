from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Playlist, Song, PlaylistSong
from .forms import AddSongForm, AddPlaylistForm, AddSongToPlaylistForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


def index(request):
    playlists = Playlist.objects.all()
    songs = Song.objects.all()
    return render(request, "SongApp/index.html", {
        "playlists": playlists,
        "songs": songs,
    })

def song_details(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Song id: {song_id} does not exist")
        return HttpResponseRedirect(reverse("SongApp:index"))
    return render(request, "SongApp/song.html", {
        "song": song
    })

@login_required(login_url="/users/login")
def add_song(request):
    if request.method == "POST":
        form = AddSongForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            artist = form.cleaned_data["artist"]
            url_field = form.cleaned_data["url_field"]
            song = Song(title=title, artist=artist, url_field=url_field, added_by=request.user)
            song.save()
            messages.success(request, "Song added successfully")
            return HttpResponseRedirect(reverse("SongApp:index"))
        else:
            return render(request, "SongApp/add_song.html",{
                "form": form
            })
    return render(request, "SongApp/add_song.html",{
        "form": AddSongForm()
    })


def playlist(request, playlist_id):
    try:
        this_playlist = Playlist.objects.get(pk=playlist_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Playlist id {playlist_id} does not exist")
        return HttpResponseRedirect(reverse("SongApp:index"))
    return render(request, "SongApp/playlist.html",{
        "playlist": this_playlist,
        "logged_in_user": request.user
    })


def add_song_to_playlist(request, playlist_id):
    form = AddSongToPlaylistForm(playlist_id, request.POST or None)
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if request.method == "POST" and form.is_valid():
        songs = form.cleaned_data["songs"]
        if not songs:
            messages.error(request, "Select at least one song to add to playlist")
            return render(request, "SongApp/add_song_to_playlist.html", {
                "form": form,
                "playlist": playlist
            })
        try:
            playlist.add_songs(songs)
            messages.success(request, "Song added to playlist successfully")
            return HttpResponseRedirect(reverse("SongApp:playlist", args=(playlist_id,)))
        except Song.DoesNotExist:
            messages.error(request, "Song does not exist")
            return render(request, "SongApp/add_song_to_playlist.html", {
                "form": form,
                "playlist": playlist
            })
        except Exception as e:
            messages.error(request, f"An error occured: {str(e)}")
            return HttpResponseRedirect(reverse("SongApp:playlist", args=(playlist_id,)))
    if request.user != playlist.created_by:
        messages.info(request, "Just creator can add songs")
        return HttpResponseRedirect(reverse("SongApp:playlist", args=(playlist_id,)))
    return render(request, "SongApp/add_song_to_playlist.html", {
        "form": form,
        "playlist": playlist
    })


@login_required(login_url="/users/login")
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
            return HttpResponseRedirect(reverse("SongApp:index"))
        except ObjectDoesNotExist as e:
            messages.error(request, f"An error occured: {str(e)}")
            new_playlist.delete()

    return render(request, "SongApp/add_playlist.html",{
            "form":form
    })


@login_required(login_url="/users/login")
def delete_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Playlist id {playlist_id} does not exist")
        return HttpResponseRedirect(reverse("SongApp:index"))
    if playlist.created_by != request.user:
        messages.error(request, "You can only delete playlist you added")
        return HttpResponseRedirect(reverse("SongApp:index"))
    playlist.delete()
    messages.info(request, "Playlist deleted succesfully")
    return HttpResponseRedirect(reverse("SongApp:index"))


@login_required(login_url="/users/login")
def delete_song(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Song id {song_id} does not exist")
        return HttpResponseRedirect(reverse("SongApp:index"))
    if song.added_by != request.user:
        messages.error(request, "You can only delete songs you added")
        return HttpResponseRedirect(reverse("SongApp:index"))
    song.delete()
    messages.success(request, "Song deleted successfully")
    return HttpResponseRedirect(reverse("SongApp:index"))


@login_required(login_url="/users/login")
def remove_song_from_playlist(request, playlist_id, song_id):
    try:
        playlist_song = PlaylistSong.objects.get(playlist_id=playlist_id, song_id=song_id)
    except ObjectDoesNotExist:
        messages.error(request, f"Song id {song_id} does not exist in playlist id {playlist_id}")
        return HttpResponseRedirect(reverse("SongApp:index"))
    if playlist_song.playlist.created_by != request.user:
        messages.error(request, "You can only remove songs from playlists you created")
        return HttpResponseRedirect(reverse("SongApp:index"))
    playlist_song.delete()
    messages.success(request, "Song removed from playlist successfully")
    return HttpResponseRedirect(reverse("SongApp:playlist", args=(playlist_id,)))