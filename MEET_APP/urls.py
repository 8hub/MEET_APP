from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("MeetApp.urls")),
    path("song_request/", include("SongRequests.urls")),
    path("users/", include("UsersApp.urls")),
]
