from django.urls import path
from . import views

app_name = "MeetApp"
urlpatterns = [
    path("", views.index, name="index"),
    path("create_meeting/", views.create_meeting, name="create_meeting"),
] 