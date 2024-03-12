import os
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class SongTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)  # Adjust based on your needs
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="user@email.com")

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(self.live_server_url + "/users/login")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("testuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpassword")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    
    def wait_for_element(self, element):
        self.browser.implicitly_wait(5)
        self.browser.find_element(By.CSS_SELECTOR, element)
    
    def wait_3(self):
        time.sleep(3)

    def test_add_song(self):
        self.login()
        self.browser.get(self.live_server_url + "/song_request/add_song")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='title']").send_keys("Test Song")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='artist']").send_keys("Test Artist")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='url_field']").send_keys("https://www.youtube.com/watch?v=123456")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("Song added successfully", self.browser.page_source)

    def test_add_playlist(self):
        pass