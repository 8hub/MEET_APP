#### GLOBALY
- [ ] Add functional tests
  - [x] UserApp
  - [x] MeetApp
  - [ ] SongRequests
    - [ ] Login -> go to `Playlist` -> add a `Song`
    - [ ] Login -> Add a `Song` to existing `Playlist`
- [ ] Add unit tests
  - [ ] UserApp
    - [x] test `User` model each field verification
  - [ ] MeetApp
    - [x] just login user can add meeting
  - [ ] SongRequests
    - [x] add a song to existing playlist
    - [x] adding a song create a M2M relation: `Song` with `Playlist` through `PlaylistSong` model
    - [x] Add a `Song` to existing `Playlist`

---
#### UserApp app
- [ ] *Send email with verification during register**

---
#### SongRequests app
- [ ] views:
  - [x] View `Playlist` with containing songs (REST) playlist/\<int:nr_playlist>
  - [x] Add a `Song` to existing playlist
  - [ ] After adding a `Song` to playlist refresh the form
  - [x] View `Song`/`Playlist` for not logged in `User`
  - [ ] Delete `Song`


---
#### MeetApp app
- [x] Assure that just logged in `User` can add a `Meeting`


---
#### DOCUMENTATION
- [ ] Logged in `User` can add a `Song` to existing `Playlist`