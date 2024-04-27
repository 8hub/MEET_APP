from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("meetapp/",       include("MeetApp.urls",  namespace="MeetApp")),
    path("songapp/", include("SongApp.urls",  namespace="SongApp")),
    path("usersapp/", include("UsersApp.urls", namespace="UsersApp")),
]
