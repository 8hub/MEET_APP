from django import forms
from SongApp.models import Song, Playlist

class AddSongForm(forms.Form):
    # required
    title = forms.CharField(label="Song Title", min_length=3, max_length=64)
    # optional
    artist = forms.CharField(label="Artist", max_length=64, required=False)
    url_field = forms.URLField(label="URL", required=False)

class AddPlaylistForm(forms.Form):
    # required
    title = forms.CharField(label="Playlist Title", min_length=3, max_length=64)
    # optional
    anonymous = forms.BooleanField(label="Anonymous", initial=False, required=False)
    songs = forms.MultipleChoiceField(label="Songs", choices=[], required=False, widget=forms.CheckboxSelectMultiple) 

    def __init__(self, *args, **kwargs):
        super(AddPlaylistForm, self).__init__(*args, **kwargs)
        self.fields['songs'].choices = [(song.id, str(song)) for song in Song.objects.all()]

class AddSongToPlaylistForm(forms.Form):
    songs = forms.MultipleChoiceField(label="Songs", choices=[], required=False, widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, playlist_id, *args, **kwargs):
        super(AddSongToPlaylistForm, self).__init__(*args, **kwargs)
        playlist = Playlist.objects.get(pk=playlist_id)
        songs_in_playlist = [playlist_song.song for playlist_song in playlist.playlistsong_set.all()]
        self.fields['songs'].choices = [(song.id, str(song)) for song in Song.objects.all() if song not in songs_in_playlist]

    def has_songs(self):
        return bool(self.fields['songs'].choices)