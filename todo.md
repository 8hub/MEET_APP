#### GLOBALY
- [ ] Add functional tests
  - [x] UserApp
  - [x] MeetApp
  - [ ] SongRequests
    - [x] Login -> go to `Playlist` -> add a `Song`
    - [x] Login -> Add a `Song` to existing `Playlist`
- [ ] Add unit tests
  - [x] UserApp
  - [x] MeetApp
  - [x] SongRequests

---
#### UserApp app
- [ ] *Send email with verification during register**
- [ ] Handle is_valid if the password is to similar to username

---
#### SongRequests app
- [ ] views:
  - [ ] After adding a `Song` to playlist refresh the form
  - [ ] Delete `Song` from `Playlist`
  - [ ] Delete `Song`


---
#### MeetApp app
- [ ] views:
  - [x] List all `Meeting`
  - [x] Click on `Meeting` on list and show the information
  - [ ] Add a `User` to `Meeting`
  - [ ] Delete `Meeting`
- [ ] models:
  - [x] add a through relation between `Meeting` and `User`, so in M2M relation each `User` can be assigned do each `Meeting` just once

---
#### DOCUMENTATION
- [ ] Logged in `User` can add a `Song` to existing `Playlist`
- [ ] 