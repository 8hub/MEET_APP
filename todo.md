#### GLOBALY
- [ ] Add functional tests
  - [x] UserApp
  - [x] MeetApp
  - [ ] SongApp
    - [x] Login -> go to `Playlist` -> add a `Song`
    - [x] Login -> Add a `Song` to existing `Playlist`
- [ ] Add unit tests
  - [x] UserApp
  - [x] MeetApp
    - [ ] delete `Meeting`
  - [ ] SongApp
    - [ ] delete `Song`
    - [ ] delete `Song` from `Playlist` (if *creator*)
    - [ ] delete added `Song` from not created `Playlist`
    - [ ] delete `Playlist` (if *creator*)

---
#### UserApp app
- [ ] *Send email with verification during register**
- [x] Handle is_valid if the password is to similar to username
- [x] After logging in redirect to MeetApp index.html
- [x] Focus cursor on 'username' when access 'login.index'

---
#### SongApp app
- [ ] views:
  - [x] Remove `Song` from `Playlist`
  - [x] Delete `Playlist` (only if `User` is creator)
  - [x] After adding a `Song` to playlist refresh the form
  - [x] Just creator of `Playlist` can add a `Song`
  - [x] Creator of `Playlist` can remove a `Song`
  - [x] Delete `Song` (only if `User` added it)
  - [x] Add a view of `Song` details


---
#### MeetApp app
- [ ] views:
  - [x] List all `Meeting`
  - [x] Click on `Meeting` on list and show the information
  - [x] Add a `User` to `Meeting`
  - [x] Delete `Meeting`
  - [x] Just creator of `Meeting` can delete it
- [ ] models:
  - [x] add a through relation between `Meeting` and `User`, so in M2M relation each `User` can be assigned do each `Meeting` just once

---
#### DOCUMENTATION
- [ ] Logged in `User` can add a `Song` to existing `Playlist`
- [ ] 