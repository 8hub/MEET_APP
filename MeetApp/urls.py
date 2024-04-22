from django.urls import path, include
from MeetApp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"meetings", views.MeetingViewSet, basename="meeting")

app_name = "MeetApp"
urlpatterns = [
    path("", include(router.urls)),
] 