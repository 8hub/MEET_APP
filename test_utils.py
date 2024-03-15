import os
import time
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MEET_APP.settings")
setup()

from django.test import TestCase
from django.contrib.auth import get_user_model

from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

User = get_user_model()

class LoggedInBaseTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="test@email.com")
        self.client.login(username="testuser", password="testpassword")
    
    def tearDown(self):
        self.client.logout()
        super().tearDown()



class FunctionalBaseTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)  # Adjust based on your needs

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="user@email.com")


    def login(self):
        self.browser.get(self.live_server_url + "/users/login")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("testuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpassword")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def wait_3(self):
        time.sleep(3)