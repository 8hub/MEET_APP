from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from MeetApp.forms import MeetingForm
from MeetApp.models import Meeting
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    all_meetings = Meeting.objects.all()
    return render(request, "MeetApp/index.html",{
        "meetings": all_meetings,
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
        Meeting.objects.create(
            creator=creator,
            name=name,
            description=description,
            date=date,
            time=time,
            location=location,
            users=users)
        messages.success(request, "Meeting created successfully")
        return HttpResponseRedirect(reverse("MeetApp:index"))
    
    return render(request, "MeetApp/create_meeting.html",{
        "form": form
    })

def meeting_details(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    return render(request, "MeetApp/meeting_details.html",{
        "meeting": meeting
    })