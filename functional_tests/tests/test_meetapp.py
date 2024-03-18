from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from test_utils import FunctionalBaseTest

class MeetAppTest(FunctionalBaseTest):

    def test_create_meeting(self):
        self.login()
        self.browser.get(self.live_server_url + "/create_meeting")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test Meeting")
        self.browser.find_element(By.CSS_SELECTOR, "textarea[name='description']").send_keys("Test Description")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='date']").send_keys("2021-12-12")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='time']").send_keys("12:00")
        self.browser.find_element(By.CSS_SELECTOR, "input[name='location']").send_keys("Test Location")
        self.browser.find_element(By.CSS_SELECTOR, "input[id='id_users_2']").click()
        self.browser.find_element(By.CSS_SELECTOR, "input[id='id_users_3']").click()
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("Meeting cannot be in the past", self.browser.page_source)
        self.browser.find_element(By.CSS_SELECTOR, "input[name='date']").clear()
        self.browser.find_element(By.CSS_SELECTOR, "input[name='date']").send_keys("2024-12-12")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("Meeting created successfully", self.browser.page_source)

    