import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from SongRequests.models import Playlist
from test_utils import FunctionalBaseTest

User = get_user_model()

class SongTest(FunctionalBaseTest):
    def wait_for_element(self, element):
        self.browser.implicitly_wait(self.DEFAULT_WAIT)
        self.browser.find_element(By.CSS_SELECTOR, element)


    def add_song(self, title, artist, url_field):
        self.browser.get(self.live_server_url + "/song_request/add_song")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='title']").send_keys(title)
        self.browser.find_element(By.CSS_SELECTOR, "input[name='artist']").send_keys(artist)
        self.browser.find_element(By.CSS_SELECTOR, "input[name='url_field']").send_keys(url_field)
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()


    def mark_song_to_add(self, song_nr):
        self.browser.find_element(By.CSS_SELECTOR, f"input[value='{song_nr}']").click()


    def test_add_song(self):
        self.login()
        self.add_song("Test Song", "Test Artist", "https://www.youtube.com/watch?v=123456")
        self.assertIn("Song added successfully", self.browser.page_source)


    def test_add_playlist_with_songs_and_modify_it(self):
        """
        Test create a playlist with songs,
        then add a new song
        """
        self.login()
        for i in range(1, 6):
            self.add_song(f"Test Song {i}", f"Test Artist {i}", f"https://www.youtube.com/watch?v={i}")

        self.browser.get(self.live_server_url + reverse("SongRequests:add_playlist"))
        self.browser.find_element(By.CSS_SELECTOR, "input[name='title']").send_keys("Test Playlist")

        self.mark_song_to_add("1")
        self.mark_song_to_add("3")
        self.assertEqual(Playlist.objects.count(), 0)
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertIn("Playlist created successfully", self.browser.page_source)
        self.assertEqual(Playlist.objects.first().songs.count(), 2)

        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        playlist_list = soup.find("ul", class_="playlist-list")
        self.assertIn("Test Playlist", playlist_list.text)
        self.assertIn("testuser", playlist_list.text)
        
        self.browser.get(self.live_server_url + reverse("SongRequests:index"))
        self.browser.find_element(By.LINK_TEXT, "Test Playlist").click()
        self.assertIn("Test Song 1 - Test Artist 1", self.browser.page_source)
        self.assertIn("Test Song 3 - Test Artist 3", self.browser.page_source)
        self.browser.find_element(By.LINK_TEXT, "Add a song").click()
        self.mark_song_to_add("2")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertEqual(Playlist.objects.first().songs.count(), 3)


    def test_redirections_add_song(self):
        self.browser.get(self.live_server_url + "/song_request/")
        self.browser.find_element(By.LINK_TEXT, "Add a song").click()
        WebDriverWait(self.browser, self.DEFAULT_WAIT).until(
            EC.url_contains("/users/login/?next=/song_request/add_song")
        )
        self.assertIn("You have to log in to add a song", self.browser.page_source)

        self.browser.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("testuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpassword")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(self.browser, self.DEFAULT_WAIT).until(
            EC.url_contains("/song_request/add_song")
        )