from rest_framework import serializers
from .models import Song, Playlist
from UsersApp.serializers import UserSerializer

class SongSerializer(serializers.ModelSerializer):
  added_by = UserSerializer(read_only=True)
  class Meta:
    model = Song
    fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
  songs = SongSerializer(many=True, read_only=True)
  created_by = UserSerializer(read_only=True)
  songs_count = serializers.IntegerField(read_only=True, source='count')
  
  class Meta:
    model = Playlist
    fields = '__all__'