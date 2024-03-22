from django import forms
from SongRequests.models import Song, Playlist

class AddSongForm(forms.Form):
    title = forms.CharField(label="Song Title", min_length=3, max_length=64)
    artist = forms.CharField(label="Artist", max_length=64, required=False)
    url_field = forms.URLField(label="URL", required=False)

class AddPlaylistForm(forms.Form):
    title = forms.CharField(label="Playlist Title", min_length=3, max_length=64)
    songs = forms.MultipleChoiceField(label="Songs", choices=[], required=False, widget=forms.CheckboxSelectMultiple) 
    anonymous = forms.BooleanField(label="Anonymous", required=False, initial=False)

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