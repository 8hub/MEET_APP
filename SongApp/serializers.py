from rest_framework import serializers
from .models import Song, Playlist, PlaylistSong
from UsersApp.serializers import UserSerializer

class SongSerializer(serializers.ModelSerializer):
  added_by = UserSerializer(read_only=True)
  class Meta:
    model = Song
    fields = '__all__'

  def create(self, validated_data):
    validated_data['added_by'] = self.context['request'].user
    return super().create(validated_data)


class PlaylistSerializer(serializers.ModelSerializer):
  songs = SongSerializer(many=True, read_only=True)
  created_by = UserSerializer(read_only=True)
  songs_count = serializers.IntegerField(read_only=True, source='count')
  
  class Meta:
    model = Playlist
    fields = '__all__'

  def create(self, validated_data):
    validated_data['created_by'] = self.context['request'].user
    songs_ids = self.context['request'].data.get('songs_ids', [])
    validated_data['songs'] = Song.objects.filter(id__in=songs_ids)
    return super().create(validated_data)

class PlaylistSongSerializer(serializers.ModelSerializer):
  class Meta:
    model = PlaylistSong
    fields = '__all__'