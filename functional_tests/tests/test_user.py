from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model


class UserTest(LiveServerTestCase):
    User = get_user_model()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)  # Adjust based on your needs
    
    def setUp(self):
        self.user = self.User.objects.create_user(username="testuser", password="testpassword", email="user@email.com")
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def login(self):
        self.browser.get(self.live_server_url + "/users/login")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys("testuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("testpassword")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    def test_user_login(self):
        self.login()
        self.assertIn("Logged in", self.browser.page_source)

    def test_user_logout(self):
        self.login()
        self.browser.find_element(By.LINK_TEXT, "UsersApp").click()
        self.browser.find_element(By.LINK_TEXT, "Logout").click()
        self.assertIn("Logged out", self.browser.page_source)

    def test_user_register(self):
        self.browser.get(self.live_server_url + "/users/register")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='username']").send_keys("newuser")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("newuser@email.com")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("n3wPas5word")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='password_confirm']").send_keys("n3wPas5word")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("Logged in", self.browser.page_source)
