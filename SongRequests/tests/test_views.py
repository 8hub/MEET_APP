from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from django import setup
from SongRequests.views import index
s
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
# setup()

class SongRequestsTestCase(TestCase):
    def test_index(self):
        index_page = HttpResponseRedirect(reverse("UsersApp:index"))
        self.assertEqual(index_page.url, "/users/")
