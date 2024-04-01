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

@login_required(login_url="/users/login")
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

    all_users = get_user_model().objects.all()
    users_not_participating = all_users.exclude(id__in=meeting.participants.all())
    
    is_creator = False
    if request.user == meeting.creator:
        is_creator = True
    
    if request.method == "POST":
        user_ids_to_delete = request.POST.getlist('delete_users')
        for user_id in user_ids_to_delete:
            MeetingParticipant.objects.filter(meeting=meeting, participant__id=user_id).delete()
        if user_ids_to_delete:
            messages.success(request, "Participants deleted successfully")
        else:
            messages.error(request, "No participants selected for deletion")

        user_ids_to_add = request.POST.getlist('add_users')
        for user_id in user_ids_to_add:
            MeetingParticipant.objects.create(
                participant=get_user_model().objects.get(id=user_id),
                meeting=meeting
            )
        return HttpResponseRedirect(reverse("MeetApp:meeting_details", args=(meeting_id,)))
    
    return render(request, "MeetApp/meeting_details.html",{
        "meeting": meeting,
        "is_creator": is_creator,
        "users_not_participating": users_not_participating
    })

@login_required(login_url="/users/login")
def delete_meeting(request, meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
        messages.error(request, f"Meeting nr {meeting_id} not found")
        return HttpResponseRedirect(reverse("MeetApp:index"))
    if request.user != meeting.creator:
        messages.error(request, "Just creator can delete the meeting")
        return HttpResponseRedirect(reverse("MeetApp:index"))
    meeting.delete()
    messages.success(request, "Meeting deleted successfully")
    return HttpResponseRedirect(reverse("MeetApp:index"))