from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from MeetApp.forms import MeetingForm
from MeetApp.models import Meeting, MeetingParticipant
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

def index(request):
    all_meetings = Meeting.objects.all()
    return render(request, "MeetApp/index.html",{
        "meetings": all_meetings,
    })

@login_required(login_url="../users/login")
def create_meeting(request):
    form = MeetingForm(request.POST or None, exclude_user=request.user)
    if request.method == "POST" and form.is_valid():
        creator = request.user
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        date = form.cleaned_data["date"]
        time = form.cleaned_data["time"]
        location = form.cleaned_data["location"]
        participants = form.cleaned_data["participants"]
        meeting = Meeting.objects.create(
            creator=creator,
            name=name,
            description=description,
            date=date,
            time=time,
            location=location)
        for participant in participants:
            if not isinstance(participant, get_user_model()):
                raise ValueError("Each participant must be a User instance")
            MeetingParticipant.objects.create(
                participant=participant,
                meeting=meeting
            )
        messages.success(request, "Meeting created successfully")
        return HttpResponseRedirect(reverse("MeetApp:index"))
    
    return render(request, "MeetApp/create_meeting.html",{
        "form": form
    })

def meeting_details(request, meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
        messages.error(request, f"Meeting nr {meeting_id} not found")
        return HttpResponseRedirect(reverse("MeetApp:index"))
    can_delete = False
    if request.user == meeting.creator:
        can_delete = True
    
    if request.method == "POST":
        user_ids_to_delete = request.POST.getlist('delete_users')
        for user_id in user_ids_to_delete:
            MeetingParticipant.objects.filter(meeting=meeting, participant__id=user_id).delete()
        if user_ids_to_delete:
            messages.success(request, "Participants deleted successfully")
        else:
            messages.error(request, "No participants selected for deletion")
        return HttpResponseRedirect(reverse("MeetApp:meeting_details", args=(meeting_id,)))
    
    return render(request, "MeetApp/meeting_details.html",{
        "meeting": meeting,
        "can_delete": can_delete,
    })