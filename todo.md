#### GLOBALY
- [ ] Add functional tests
  - [ ] UserApp
    - [ ] add user and add a song with this user
- [ ] Add unit tests
  - [ ] UserApp
    - [ ] test_model
      - [ ] add user
  - [ ] MeetApp
    - [ ] add meeting
  - [ ] SongRequests

---
#### UserApp app
- [x] Manage login
- [x] Manage logout
- [ ] *Send email*

---
#### SongRequests app
- [ ] views:
  - [ ] Manage `Song` just for logged in `User`
  - [ ] View `Song`/`Playlist` for not logged in `User`
  - [x] Add `Song`
  - [ ] Delete `Song`
  - [ ] Make `Playlist`
- [x] models
  - [x] Add field to `Song`:
    - [x] `add_date`
  - [x] Add field to `Playlist`:
    - [x] `add_date`
    - [x] `last_modified_date`


---
#### MeetApp app
- [ ] Add `Meeting` model with:
  - [ ] `creator` ForeignKey
  - [ ] `participants` ManyToMany
  - [ ] `playlist` ForeignKey
  - [ ] `title` 
  - [ ] `location`
  - [ ] `date`
  - [ ] `created_date`
  - [ ] `last_modified_date`
- [ ] Logged in `User` can add a `Meeting`


---
#### DOCUMENTATION

- [ ] describe models.py <--