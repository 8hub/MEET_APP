import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from SongRequests.models import Playlist

User = get_user_model()

class SongTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)  # Adjust based on your needs
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="user@email.com")

    def tearDown(self):
        self.browser.quit()
    
    def wait_for_element(self, element):
        self.browser.implicitly_wait(5)
        self.browser.find_element(By.CSS_SELECTOR, element)
    
    def wait_3(self):
        time.sleep(3)

    def add_song(self, title, artist, url_field):
        self.browser.get(self.live_server_url + "/song_request/add_song")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='title']").send_keys(title)
        self.browser.find_element(By.CSS_SELECTOR, "input[name='artist']").send_keys(artist)
        self.browser.find_element(By.CSS_SELECTOR, "input[name='url_field']").send_keys(url_field)
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def login(self):
        self.browser.get(self.live_server_url + "/users/login")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("testuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpassword")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def mark_song_to_add(self, song_id):
        self.browser.find_element(By.ID, f"id_songs_{song_id}").click()

    def test_add_song(self):
        self.login()
        self.add_song("Test Song", "Test Artist", "https://www.youtube.com/watch?v=123456")
        self.assertIn("Song added successfully", self.browser.page_source)

    def test_add_playlist(self):
        self.login()
        # add 5 test songs
        for i in range(1, 6):
            self.add_song(f"Test Song {i}", f"Test Artist {i}", f"https://www.youtube.com/watch?v={i}")

        self.browser.get(self.live_server_url + reverse("SongRequests:add_playlist"))
        self.browser.find_element(By.CSS_SELECTOR, "input[name='title']").send_keys("Test Playlist")

        self.mark_song_to_add("1")
        self.mark_song_to_add("3")

        self.assertEqual(Playlist.objects.count(), 0)
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.wait_3()
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertIn("Playlist created successfully", self.browser.page_source)