from django.urls import path, include
from SongApp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"songs", views.SongViewSet, basename="song")
router.register(r"playlists", views.PlaylistViewSet, basename="playlist")

app_name = "SongApp"
urlpatterns = [
  path("", include(router.urls)),
]
