from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserDetailView, RefreshAccessTokenView

app_name = "UsersApp"
urlpatterns = [
    path('', UserDetailView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshAccessTokenView.as_view(), name='refresh'),
]
