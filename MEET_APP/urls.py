from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("RootApp.urls")),
    path("meet/", include("MeetApp.urls",  namespace="MeetApp")),
    path("music/", include("SongApp.urls",  namespace="SongApp")),
    path("user/", include("UsersApp.urls", namespace="UsersApp")),
    # Serve React frontend
    path("", TemplateView.as_view(template_name="index.html")),
    # Add a catch-all pattern at the end of all other patterns
    re_path(r'^.*$', lambda request: HttpResponseRedirect('/api/'), name='catch-all'),
]
