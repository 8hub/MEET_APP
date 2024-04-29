from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponseRedirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("RootApp.urls")),
    path("meet/", include("MeetApp.urls",  namespace="MeetApp")),
    path("music/", include("SongApp.urls",  namespace="SongApp")),
    path("user/", include("UsersApp.urls", namespace="UsersApp")),
    # Add a catch-all pattern at the end of all other patterns
    re_path(r'^.*$', lambda request: HttpResponseRedirect('/api/'), name='catch-all'),
]
