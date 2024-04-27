from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Playlist, Song, PlaylistSong
from .forms import AddSongForm, AddPlaylistForm, AddSongToPlaylistForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlaylistSerializer, SongSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @action(detail=True, methods=['get'])
    def get_playlists(self, request, pk=None):
        song = self.get_object()
        playlists = song.get_playlists()
        return Response(PlaylistSerializer(playlists, many=True).data)
    
    @action(detail=True, methods=['post'])
    def add_to_playlist(self, request, pk=None):
        song = self.get_object()
        playlist_id = request.data.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.add_songs([song.id])
            playlists = song.get_playlists()
            return Response(PlaylistSerializer(playlists, many=True).data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"error": "Playlist does not exist"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_from_playlist(self, request, pk=None):
        song = self.get_object()
        playlist_id = request.data.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.remove_songs([song.id])
            playlists = song.get_playlists()
            return Response(PlaylistSerializer(playlists, many=True).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Playlist does not exist"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def update_artist(self, request, pk=None):
        song = self.get_object()
        artist = request.data.get('artist')
        if not artist:
            return Response({"error": "Artist is required"}, status=status.HTTP_400_BAD_REQUEST)
        song.artist = artist
        song.save()
        return Response(SongSerializer(song).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_title(self, request, pk=None):
        song = self.get_object()
        title = request.data.get('title')
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        song.title = title
        song.save()
        return Response(SongSerializer(song).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_url(self, request, pk=None):
        song = self.get_object()
        url_field = request.data.get('url_field')
        if not url_field:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        song.url_field = url_field
        song.save()
        return Response(SongSerializer(song).data, status=status.HTTP_200_OK)
    
    
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer   

    @action(detail=True, methods=['get'])
    def get_songs(self, request, pk=None):
        playlist = self.get_object()
        songs = playlist.songs.all()
        return Response(SongSerializer(songs, many=True).data)
    
    @action(detail=True, methods=['post'])
    def add_songs(self, request, pk=None):
        playlist = self.get_object()
        song_ids = request.data.get('song_ids')
        # song_ids must be a list
        if not isinstance(song_ids, list):
            return Response({"error": "song_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            playlist.add_songs(song_ids)
            songs = playlist.songs.all()
            return Response(SongSerializer(songs, many=True).data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"error": "Song does not exist"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_songs(self, request, pk=None):
        playlist = self.get_object()
        song_ids = request.data.get('song_ids')
        # song_ids must be a list
        if not isinstance(song_ids, list):
            return Response({"error": "song_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            playlist.remove_songs(song_ids)
            songs = playlist.songs.all()
            return Response(SongSerializer(songs, many=True).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Song does not exist"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def update_title(self, request, pk=None):
        playlist = self.get_object()
        title = request.data.get('title')
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        playlist.title = title
        playlist.save()
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_200_OK)
