from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "MeetApp/index.html",{
        "hello": ["Hey", "Hi", "Hello"]
    })
