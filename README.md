- [Backend models](#backend-models)
  - [MeetApp models](#meetapp-models)
    - [`Meeting` model](#meeting-model)
    - [`MeetingParticipant` model (intermediary model)](#meetingparticipant-model-intermediary-model)
  - [UserApp models](#userapp-models)
    - [`CustomUser` model](#customuser-model)
  - [SongApp models](#songapp-models)
    - [`Song` model](#song-model)
    - [`Playlist` model](#playlist-model)
    - [`PlaylistSong` model (intermediary model)](#playlistsong-model-intermediary-model)
- [API documentation - Backend](#api-documentation---backend)
  - [MeetingViewSet API Endpoints](#meetingviewset-api-endpoints)
    - [`GET /meetings/`](#get-meetings)
    - [`GET /meetings/{id}/`](#get-meetingsid)
    - [`POST /meetings/`](#post-meetings)
    - [`PUT /meetings/{id}/`](#put-meetingsid)
    - [`DELETE /meetings/{id}/`](#delete-meetingsid)
    - [`POST /meetings/{id}/add_participant/`](#post-meetingsidadd_participant)
    - [`POST /meetings/{id}/remove_participant/`](#post-meetingsidremove_participant)
    - [`POST /meetings/{id}/clear_participants/`](#post-meetingsidclear_participants)
    - [`GET /meetings/{id}/get_participants/`](#get-meetingsidget_participants)
    - [`GET /meetings/{id}/get_participant_ids/`](#get-meetingsidget_participant_ids)
  - [User API Endpoints](#user-api-endpoints)
    - [`POST /register/`](#post-register)
    - [`POST /login/`](#post-login)
    - [`POST /logout/`](#post-logout)
    - [`GET /user/`](#get-user)
  - [SongApp API](#songapp-api)
    - [`GET /songs/`](#get-songs)
    - [`POST /songs/`](#post-songs)
    - [`GET /songs/{id}/`](#get-songsid)
    - [`PUT /songs/{id}/`](#put-songsid)
    - [`DELETE /songs/{id}/`](#delete-songsid)
    - [`GET /songs/{id}/get_playlists/`](#get-songsidget_playlists)
    - [`POST /songs/{id}/add_to_playlist/`](#post-songsidadd_to_playlist)
    - [`POST /songs/{id}/remove_from_playlist/`](#post-songsidremove_from_playlist)
    - [`PUT /songs/{id}/update_artist/`](#put-songsidupdate_artist)
    - [`PUT /songs/{id}/update_title/`](#put-songsidupdate_title)
    - [`PUT /songs/{id}/update_url/`](#put-songsidupdate_url)
    - [`GET /playlists/`](#get-playlists)
    - [`POST /playlists/`](#post-playlists)
    - [`GET /playlists/{id}/`](#get-playlistsid)
    - [`PUT /playlists/{id}/`](#put-playlistsid)
    - [`DELETE /playlists/{id}/`](#delete-playlistsid)
    - [`GET /playlists/{id}/get_songs/`](#get-playlistsidget_songs)
    - [`POST /playlists/{id}/add_songs/`](#post-playlistsidadd_songs)
    - [`POST /playlists/{id}/remove_songs/`](#post-playlistsidremove_songs)
    - [`PUT /playlists/{id}/update_title/`](#put-playlistsidupdate_title)
- [API documentation - Frontend](#api-documentation---frontend)
  - [Features](#features)
- [License](#license)

# Backend models

## MeetApp models

### `Meeting` model


```python
class Meeting(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_meetings")
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=64)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='MeetingParticipant', blank=True, related_name="meetings")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
```

### `MeetingParticipant` model (intermediary model)

```python
class MeetingParticipant(models.Model):
    '''
    Additional model to crate a intermediary table
    for the many-to-many relationship between
    `Meeting` and `User` models
    '''
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('participant', 'meeting')
        verbose_name = "Meeting Participant"
        verbose_name_plural = "Meeting Participants"
```

## UserApp models

### `CustomUser` model
```python
class CustomUser(AbstractUser):
    pass
    # ALL BELOW ARE INHERITED FROM AbstractUser
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group, related_name="user_set",   related_query_name="user")
    user_permissions = models.ManyToManyField(Permission,   related_name="user_set", related_query_name="user")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
```

## SongApp models

### `Song` model
```python
class Song(models.Model):
    title = models.CharField(max_length=64)
    artist = models.CharField(max_length=64, blank=True, null=True)
    url_field = models.URLField(max_length=200, blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="songs")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
```

### `Playlist` model
```python
class Playlist(models.Model):
    title = models.CharField(max_length=64, unique=True)
    songs = models.ManyToManyField('Song', through='PlaylistSong', blank=True, related_name="parent_playlists")
    anonymous = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="playlists")
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
```

### `PlaylistSong` model (intermediary model)
```python
class PlaylistSong(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['add_date']
        unique_together = (('playlist', 'song'),)
```

# API documentation - Backend
The app is devided into 3 apps:
1. `MeetApp` - API  for sending and receiving info about meetings
2. `UserApp` - API for sending and receiving info about users
3. `SongApp` - API for sending and receiving info about song requests

## MeetingViewSet API Endpoints

### `GET /meetings/`
- Returns a list of all meetings.
- Response status: 200 OK

### `GET /meetings/{id}/`
- Returns the details of a specific meeting by its ID.
- Response status: 200 OK

### `POST /meetings/`
- Creates a new meeting.
- Response status: 201 Created

### `PUT /meetings/{id}/`
- Updates the details of a specific meeting by its ID.
- Response status: 200 OK

### `DELETE /meetings/{id}/`
- Deletes a specific meeting by its ID.
- Response status: 204 No Content

### `POST /meetings/{id}/add_participant/`
- Adds a participant to a specific meeting by its ID.
- Request body should include `user_id`.
- Response status: 201 Created if successful, 404 Not Found if user does not exist.

### `POST /meetings/{id}/remove_participant/`
- Removes a participant from a specific meeting by its ID.
- Request body should include `user_id`.
- Response status: 200 OK if successful, 404 Not Found if user does not exist.

### `POST /meetings/{id}/clear_participants/`
- Clears all participants from a specific meeting by its ID.
- Response status: 200 OK

### `GET /meetings/{id}/get_participants/`
- Returns a list of all participants in a specific meeting by its ID.
- Response status: 200 OK

### `GET /meetings/{id}/get_participant_ids/`
- Returns a list of all participant IDs in a specific meeting by its ID.
- Response status: 200 OK

## User API Endpoints

### `POST /register/`
- Registers a new user.
- Request body should include `username`, `email`, and `password`.
- Returns a `refresh` and `access` token upon successful registration.
- Response status: 201 Created if successful, 422 Unprocessable Entity if email or password is invalid, 400 Bad Request for other errors.

### `POST /login/`
- Logs in an existing user.
- Request body should include `username` and `password`.
- Returns a `refresh`, `access` token and `user` upon successful login:
```json
  {
    "refresh": "<refresh_token_hash>",
    "access": "<access_token_hash>",
    "user": {
        "id": <int>,
        "username": <string>,
        "email": <string>
    }
}
```
- Response status: 200 OK if successful, 401 Unauthorized if credentials are invalid.

### `POST /logout/`
- Logs out an authenticated user.
- Request body should include the `refresh` token.
- Blacklists the `refresh` token.
- Response status: 205 Reset Content if successful, 400 Bad Request if an error occurred.

### `GET /user/`
- Returns the details of the authenticated user.
- Response status: 200 OK

## SongApp API
***`Song` model views***
### `GET /songs/`
- Lists all songs.
- No authentication or permissions required.

### `POST /songs/`
- Creates a new song.
- Requires authentication and the user must be the owner of the song.

### `GET /songs/{id}/`
- Retrieves a specific song by its ID.
- No authentication or permissions required.

### `PUT /songs/{id}/`
- Updates a specific song.
- Requires authentication and the user must be the owner of the song.

### `DELETE /songs/{id}/`
- Deletes a specific song.
- Requires authentication and the user must be the owner of the song.

### `GET /songs/{id}/get_playlists/`
- Retrieves all playlists that a specific song is part of.
- No authentication or permissions required.

### `POST /songs/{id}/add_to_playlist/`
- Adds a specific song to a playlist.
- Requires authentication and the user must be the owner of the song.

### `POST /songs/{id}/remove_from_playlist/`
- Removes a specific song from a playlist.
- Requires authentication and the user must be the owner of the song.

### `PUT /songs/{id}/update_artist/`
- Updates the artist of a specific song.
- Requires authentication and the user must be the owner of the song.

### `PUT /songs/{id}/update_title/`
- Updates the title of a specific song.
- Requires authentication and the user must be the owner of the song.

### `PUT /songs/{id}/update_url/`
- Updates the URL of a specific song.
- Requires authentication and the user must be the owner of the song.

---
***`Playlist` model views***

### `GET /playlists/`
- Lists all playlists - JSON of [`GET /playlists/{id}/`](#get-playlistsid) responses.
- No authentication or permissions required.

### `POST /playlists/`
- Creates a new playlist.
- Requires authentication and the user must be the creator of the playlist.

### `GET /playlists/{id}/`
- Retrieves a specific playlist by its ID.
- No authentication or permissions required.
```json
{
    "id": <int>, // playlist ID
    "songs": [
        {
            "id": <int>,
            "added_by": <null> or {
                "id": <int>,
                "username": <string>,
                "email": <string>
            },
            "title": <string>,
            "artist": <string>,
            "url_field": <string>, // URL with http:// or https:// prefix
            "add_date": <string> // format is "YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM"
        }
    ],
    "created_by": { <null> or {
        "id": <int>,
        "username": <string>,
        "email": <string>
    },
    "songs_count": <int>,
    "title": <string>,
    "anonymous": <bool>,
    "add_date": <string>, // format is "YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM"
    "last_modified": <string> // format is "YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM"
}
```

### `PUT /playlists/{id}/`
- Updates a specific playlist.
- Requires authentication and the user must be the creator of the playlist.

### `DELETE /playlists/{id}/`
- Deletes a specific playlist.
- Requires authentication and the user must be the creator of the playlist.

### `GET /playlists/{id}/get_songs/`
- Retrieves all songs in a specific playlist.
- No authentication or permissions required.

### `POST /playlists/{id}/add_songs/`
- Adds songs to a specific playlist.
- Requires authentication and the user must be the creator of the playlist.

### `POST /playlists/{id}/remove_songs/`
- Removes songs from a specific playlist.
- Requires authentication and the user must be the creator of the playlist.

### `PUT /playlists/{id}/update_title/`
- Updates the title of a specific playlist.
- Requires authentication and the user must be the creator of the playlist.

# API documentation - Frontend

## Features

- User authentication
- Event creation and management
- Real-time updates and notifications
- Integration with the MeetApp backend API


# License

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). You are free to share (copy and redistribute the material in any medium or format) and adapt (remix, transform, and build upon the material for any purpose, even commercially), under the following terms: Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.