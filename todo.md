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
    - [ ] delete `Meeting`
  - [ ] SongRequests
    - [ ] delete `Song`
    - [ ] delete `Song` from `Playlist`

---
#### UserApp app
- [ ] *Send email with verification during register**
- [x] Handle is_valid if the password is to similar to username
- [ ] After logging in redirect to MeetApp index.html
- [ ] Focus cursor on 'username' when access 'login.index'

---
#### SongRequests app
- [ ] views:
  - [ ] After adding a `Song` to playlist refresh the form
  - [ ] Just creator of `Playlist` can add a `Song`
  - [ ] Just creator of `Playlist` can delete a `Song`
  - [ ] Delete `Song` from `Playlist`
  - [ ] Delete `Song`


---
#### MeetApp app
- [ ] views:
  - [x] List all `Meeting`
  - [x] Click on `Meeting` on list and show the information
  - [x] Add a `User` to `Meeting`
  - [x] Delete `Meeting`
- [ ] models:
  - [x] add a through relation between `Meeting` and `User`, so in M2M relation each `User` can be assigned do each `Meeting` just once

---
#### DOCUMENTATION
- [ ] Logged in `User` can add a `Song` to existing `Playlist`
- [ ] 