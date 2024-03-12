- [ ] describe the models and their connection

---

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


# 1. Introduction
This is a simple app that allows you to create and manage meetings. It contain 3 separate apps:
- **MeetApp**: This app is responsible for creating and managing meetings.
- **UsersApp**: This app is responsible for creating and managing users.
- **SongRequests**: This app is responsible for creating and managing songs and playlists.



## 1.1. MeetApp
This app is responsible for creating and managing meetings. It contains the following models:

## 1.2. UsersApp
This app is responsible for creating and managing users. It contains the following models:

## 1.3. SongRequests
This app is responsible for creating and managing songs and playlists. It contains the following models:

---
# 2. models.py
## 2.1. MeetApp
No models for now

## 2.2. UsersApp
Created custom `User` with plan for future update.\
To access the `User` in each app the `AUTH_USER_MODEL = "UsersApp.User"` was added to `settings.py`
To access `User`:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

```python
class User(AbstractUser):
  '''Plan to modify in the future
  Add followers etc.'''
  pass
```


## 2.3. SongRequests
```python
class Song(models.Model):
  title = models.CharField(max_length=64)
  artist = models.CharField(max_length=64, blank=True, null=True)
  url_field = models.URLField(max_length=200, blank=True, null=True)
  added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="songs")

class Playlist(models.Model):
  name = models.CharField(max_length=64)
  songs = models.ManyToManyField(Song, blank=True, related_name="parent_playlists")
  anonymous = models.BooleanField(default=False)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="playlists")

```

# 3. tests

## 3.1. unit tests
To each app directory was added *test* folder in which are placed tests:
- test_views.py
- test_models.py
- test_templates.py

`from django.test import TestCase` is not supported by `unittest`, so `pytest-django` have to be installed to run tests in *VSCode Test Explorer*

To enable running tests in VSCode to each test was added suffix:

```python
import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()
```
