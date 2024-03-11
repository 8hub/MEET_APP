from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "MeetApp/hello.html",{
        "hello": ["Hey", "Hi", "Hello"]
    })
