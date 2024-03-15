from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from MeetApp.forms import MeetingForm
from MeetApp.models import Meeting
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "MeetApp/index.html",{
        "hello": ["Hey", "Hi", "Hello"]
    })

@login_required(login_url="../users/login")
def create_meeting(request):
    form = MeetingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        creator = request.user
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        date = form.cleaned_data["date"]
        time = form.cleaned_data["time"]
        location = form.cleaned_data["location"]
        users = form.cleaned_data["users"]
        new_meeting = Meeting.objects.create(
            creator=creator, name=name, description=description,
            date=date, time=time, location=location)
        new_meeting.users.set(users)
        messages.success(request, "Meeting created successfully")
        return HttpResponseRedirect(reverse("MeetApp:index"))
    
    return render(request, "MeetApp/create_meeting.html",{
        "form": form
    })