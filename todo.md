#### GLOBALY
- [ ] Add functional tests
  - [ ] UserApp
  - [ ] MeetApp
  - [ ] SongRequests
    - [ ] Login -> go to `Playlist` -> add a `Song`
- [ ] Add unit tests
  - [ ] UserApp
    - [ ] test `User` model each field verification
  - [ ] MeetApp
    - [ ] just login user can add meeting
  - [ ] SongRequests
    - [ ] add a song to existing playlist
    - [ ] adding a song create a M2M relation: `Song` with `Playlist` through `PlaylistSong` model

---
#### UserApp app
- [ ] *Send email with verification during register**

---
#### SongRequests app
- [ ] views:
  - [x] View `Playlist` with containing songs (REST) playlist/\<int:nr_playlist>
  - [ ] Add a `Song` to existing playlist
  - [x] View `Song`/`Playlist` for not logged in `User`
  - [ ] Delete `Song`


---
#### MeetApp app
- [x] Assure that just logged in `User` can add a `Meeting`


---
#### DOCUMENTATION
