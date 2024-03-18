from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

class TopBarLinksTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(5)  # Adjust based on your needs

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_top_bar_links_text(self):
        self.browser.get(self.live_server_url)

        top_bar = self.browser.find_element(By.CLASS_NAME, 'top_bar')
        links = top_bar.find_elements(By.TAG_NAME, 'a')
        link_texts = [link.text for link in links]

        self.assertEqual(link_texts, ["MeetApp", "SongRequests", "UsersApp"], "The top-bar links text did not match the expected values")
    

    def test_title_and_header(self):
        self.browser.get(self.live_server_url)
        self.assertIn('MeetApp', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('MeetApp', header_text)
