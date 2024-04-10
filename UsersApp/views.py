from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import NewUserForm

User_model = get_user_model()

def index(request):
    if not request.user.is_authenticated:
        return login_views(request)
    else:
        return render(request, "UsersApp/index.html", {
            "user": request.user
        })
    
def login_views(request):
    redirect_to = request.POST.get('next') or request.GET.get("next", "")
    if redirect_to == "/song_request/add_song":
        messages.info(request, "You have to log in to add a song")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Logged in.")
            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            return HttpResponseRedirect(reverse("MeetApp:index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "UsersApp/login.html",{
                "next": redirect_to
            })
            
    return render(request, "UsersApp/login.html", {
        "next": redirect_to
    })

def logout_views(request):
    logout(request)
    messages.info(request, "Logged out.")
    return render(request, "UsersApp/login.html")


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # validate all fields - important
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User_model.objects.create_user(username, email, password)
            login(request, user)
            messages.info(request, "Logged in.")
            return HttpResponseRedirect(reverse("UsersApp:index"))
        else:
            return render(request, "UsersApp/register.html", {
                "form": form
            })
    else:
        form = NewUserForm()
        return render(request, "UsersApp/register.html", {
            "form": form
        })