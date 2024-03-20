import time
from django.test import TestCase
from django.contrib.auth import get_user_model

from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

class LoggedInUnitBaseTest(TestCase):    
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword", email="test@email.com")
        get_user_model().objects.create_user(username="testuser2", password="testpassword", email="test2@email.com")
        get_user_model().objects.create_user(username="testuser3", password="testpassword", email="test3@email.com")
        get_user_model().objects.create_user(username="testuser4", password="testpassword", email="test4@email.com")
        get_user_model().objects.create_user(username="testuser5", password="testpassword", email="test5@email.com")
        self.client.login(username="testuser", password="testpassword")
    
    def tearDown(self):
        self.client.logout()
        super().tearDown()

    def get_user_instance(self):
        User = get_user_model()
        return User()


class FunctionalBaseTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword", email="user@email.com")
        get_user_model().objects.create_user(username="testuser2", password="testpassword", email="test2@email.com")
        get_user_model().objects.create_user(username="testuser3", password="testpassword", email="test3@email.com")
        get_user_model().objects.create_user(username="testuser4", password="testpassword", email="test4@email.com")
        get_user_model().objects.create_user(username="testuser5", password="testpassword", email="test5@email.com")


    def login(self):
        self.browser.get(self.live_server_url + "/users/login")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("testuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpassword")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def wait_3(self):
        time.sleep(3)