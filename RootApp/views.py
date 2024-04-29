from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse as api_reverse

class APIRootView(APIView):
    """
    API Root view that lists all apps endpoints.
    """
    def get(self, request, format=None):
        return Response({
            'meetings': api_reverse('MeetApp:meeting-list', request=request, format=format),
            'songs': api_reverse('SongApp:song-list', request=request, format=format),
            'playlists': api_reverse('SongApp:playlist-list', request=request, format=format),
            'register': api_reverse('UsersApp:register', request=request, format=format),
            'login': api_reverse('UsersApp:login', request=request, format=format),
            'logout': api_reverse('UsersApp:logout', request=request, format=format),
            'user_detail': api_reverse('UsersApp:user_detail', request=request, format=format),
        })
