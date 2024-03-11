from django.urls import path
from . import views

app_name = "UsersApp"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_views, name="login"),
    path("logout/", views.logout_views, name="logout"),
]