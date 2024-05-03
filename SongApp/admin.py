from django.contrib import admin

from .models import Song, Playlist, PlaylistSong

class PlaylistSongInline(admin.TabularInline):
  model = PlaylistSong
  extra = 1
  fk_name = 'playlist'
  verbose_name = 'Song'
  verbose_name_plural = 'Songs'
  fields = ['song']
  show_change_link = True
  extra = 0

class PlaylistInline(admin.TabularInline):
  model = PlaylistSong
  extra = 1
  fk_name = 'song'
  verbose_name = 'Playlist'
  verbose_name_plural = 'Playlists'
  fields = ['playlist']
  show_change_link = True
  extra = 0

class SongAdmin(admin.ModelAdmin):
  inlines = [PlaylistInline]

class PlaylistAdmin(admin.ModelAdmin):
  inlines = [PlaylistSongInline]

admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)