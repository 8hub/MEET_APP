#### GLOBALY
- [ ] Add functional tests
- [ ] Add unit tests

---
#### UserApp app
- [ ] Manage login
- [ ] Manage logout
- [ ] *Send email*

---
#### SongRequests app
- [ ] Manage `Song` just for logged in `User`
- [ ] View `Song`/`Playlist` for not logged in `User`
- [ ] Add `Song`
- [ ] Delete `Song`
- [ ] Make `Playlist`
- [ ] Add field to `Song`:
  - [ ] `add_date`
- [ ] Add field to `Playlist`:
  - [ ] `add_date`
  - [ ] `last_modified_date`


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

- [ ] describe models.py