- [1. Introduction](#1-introduction)
  - [1.1. MeetApp](#11-meetapp)
  - [1.2. UsersApp](#12-usersapp)
  - [1.3. SongRequests](#13-songrequests)
- [2. models.py](#2-modelspy)
  - [2.1. MeetApp](#21-meetapp)
  - [2.2. UsersApp](#22-usersapp)
  - [2.3. SongRequests](#23-songrequests)
- [3. tests](#3-tests)
  - [3.1. unit tests](#31-unit-tests)
    - [3.1.1. MeetApp](#311-meetapp)
    - [3.1.2. SongRequests](#312-songrequests)
    - [3.1.3. UsersApp](#313-usersapp)
  - [3.2. functional tests](#32-functional-tests)
    - [3.2.1. test\_loading.py](#321-test_loadingpy)
    - [3.2.2. test\_songrequests.py](#322-test_songrequestspy)
    - [3.2.3. test\_user.py](#323-test_userpy)
    - [3.2.4. test\_meetapp.py](#324-test_meetapppy)


# 1. Introduction
This is a simple app that allows you to create and manage meetings. It contain 3 separate apps:
- **MeetApp**: This app is responsible for creating and managing meetings.
- **UsersApp**: This app is responsible for creating and managing users.
- **SongRequests**: This app is responsible for creating and managing songs and playlists.



## 1.1. MeetApp
This app is responsible for creating and managing meetings. It contains the following models:
- `Meeting`

## 1.2. UsersApp
This app is responsible for creating and managing users. It contains the following models:
- `User`

## 1.3. SongRequests
This app is responsible for creating and managing songs and playlists. It contains the following models:
- `Song`
- `Playlist`
- `SongPlaylist` - *links the `Song` to `Playlist`*

---
# 2. models.py
## 2.1. MeetApp
```python
class Meeting(models.Model):
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_meetings")
  name = models.CharField(max_length=64)
  description = models.TextField(blank=True, null=True)
  date = models.DateField()
  time = models.TimeField()
  location = models.CharField(max_length=64)
  users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="meetings")
  add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  last_modified = models.DateTimeField(auto_now=True)
```

## 2.2. UsersApp
To validate a `username`, `email` and `password` in the model layer the `CustomUserManager` class was added. With this approach even the `User` that is created programmatically - batch script, admin or APIs - will be validated.
```python
class CustomUserManager(BaseUserManager)
```

```python
class User(AbstractUser):
    objects = CustomUserManager()
```

`User` inherit form `AbstractUser`, so it can be customized.\
The `AUTH_USER_MODEL = "UsersApp.User"` was added to `settings.py` so in each app `User` can be accessed through `get_user_model()` method:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```


## 2.3. SongRequests
```python
class Song(models.Model):
  title = models.CharField(max_length=64)
  artist = models.CharField(max_length=64,blank=True, null=True)
  url_field = models.URLField(max_length=200,blank=True, null=True)
  added_by = models.ForeignKey(settingsAUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, related_name="songs")
  add_date = models.DateTimeFiel(auto_now_add=True, blank=True, null=True)

class Playlist(models.Model):
  title = models.CharField(max_length=64, unique=True)
  songs = models.ManyToManyField('Song',through='PlaylistSong', blank=True,related_name="parent_playlists")
  anonymous = models.BooleanField(default=False)
  created_by = models.ForeignKey(settingsAUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, blank=True, related_name="playlists")
  add_date = models.DateTimeFiel(auto_now_add=True, blank=True, null=True)
  last_modified = models.DateTimeFiel(auto_now=True)

class PlaylistSong(models.Model):
  '''
  represents link from Song to Playlist with 'add_date' parameter
  to track the date of  changes in playlist
  '''
  playlist = models.ForeignKey('Playlist',on_delete=models.CASCADE)
  song = models.ForeignKey('Song',on_delete=models.CASCADE)
  add_date = models.DateTimeFiel(auto_now_add=True)
```
During creation of the model `Playlist` on the model the validation was added - if the `Playlist` with the same title exist, do not create another one:
```python
def save(self, *args, **kwargs):
  if self.title:
    if self.title in Playlist.objects.values_list('title', flat=True):
      raise IntegrityError("Playlist with this title already exists.")
    super().save(*args, **kwargs)
  else:
    raise ValueError("Playlist must have a title.")
```
# 3. tests

## 3.1. unit tests
To each app directory was added *test* folder in which are placed tests:
- test_views.py
- test_models.py
- test_templates.py

`from django.test import TestCase` is not supported by `unittest`, so `pytest-django` have to be installed to run tests in *VSCode Test Explorer*.

To enable running tests in VSCode the `pytest.ini` had to be configured:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = MEET_APP.settings
python_files = tests.py test_*.py *_tests.py
```

Testing `models.py` cannot be done using VSCode *Test Explorer* without importing models inside each `test_method()`. Because of that, to stick with maintainability of the code, each `test_models.py` file will be run through **django-test framework**.

### 3.1.1. MeetApp
- test_views.py
  - redirection to `MeetApp:index`
  - status code of `MeetApp:index`
  - template used for `MeetApp:index`
- test_models.py
  - create a `Meeting`
  - add `User` to `Meeting`
  - remove `User` from `Meeting`
  - clear `Meeting` from `Users`


### 3.1.2. SongRequests
- test_views.py
  - load `SongRequests:index`
  - load `SongRequests:add_song`
  - logged in `User` can add a `Song`
  - if `User` want to add a `Song` and is not logged in redirect to `UserApp/login.html`
- test_models.py
  - test creation of `Song` with all required fields
  - test creation of `Song` without title
  - test creation of `Song` without artist and URL
  - test creation of `Playlist` with all required fields
  - test creation of `Playlist` without title
  - test creation of `Playlist` with the same title
  - test adding `Song` to existing `Playlist`
  - test creation of `Playlist` 
  - create a `Song`
### 3.1.3. UsersApp
- test_views.py
  - test index view
  - test login view
  - test login view redirection after logging in
- test_models.py
  - create `User` with correct data
  - test creation of `User` with no username
  - test creation of `User` with no email
  - test creation of `User` with no password
  - test creation of `User` with invalid email
  - test creation of `User` with invalid password
  - 


## 3.2. functional tests
### 3.2.1. test_loading.py
- top bar loading
- title and header

### 3.2.2. test_songrequests.py
- login and add `Song`
- login, add 5 `Song` and create `Playlist`
- when not logged in `User` try to add a song he is redirected to `UsersApp` to log in and when he log in next redirection go to `SongRequests:add_song`

### 3.2.3. test_user.py
Test the functionality of UsersApp:
- login `User`
- logout `User`
- register `User`

### 3.2.4. test_meetapp.py
Test the functionality of MeetApp:
- logged in `User` cannot create a meeting in the past, but can create a meeting in the future