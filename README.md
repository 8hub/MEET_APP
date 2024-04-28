- [API documentation](#api-documentation)
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
## API documentation
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
- Returns a `refresh` and `access` token upon successful login.
- Response status: 200 OK if successful, 401 Unauthorized if credentials are invalid.

### `POST /logout/`
- Logs out an authenticated user.
- Request body should include the `refresh` token.
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
- Lists all playlists.
- No authentication or permissions required.

### `POST /playlists/`
- Creates a new playlist.
- Requires authentication and the user must be the creator of the playlist.

### `GET /playlists/{id}/`
- Retrieves a specific playlist by its ID.
- No authentication or permissions required.

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