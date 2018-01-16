from os import environ
from time import sleep

from django.contrib.auth.models import User
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from daily_quote.models import Profile, Quote, QuoteRank
#from quote_me.tests import FunctionalTestCase


class DailyQuoteTests(TestCase):
    fixtures = ['author', 'quote']

    def setUp(self):
        User.objects.create_user('alice', 'alice@gmail.com', 'pass1234')
        User.objects.create_user('bob', 'bob@gmail.com', 'pass1234')

    def test_user_quote_rendered_to_home_page(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/')

        profile = Profile.objects.get(user__username='alice')
        quote = response.context['quote']

        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote, profile.current_quote)

    def test_user_quote_rendered_to_profile_page(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/alice/')

        profile = Profile.objects.get(user__username='alice')
        quote = response.context['quote']

        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote, profile.current_quote)

    def test_anonymous_user_quote_rendered_to_home(self):
        response = self.client.get('/')
        quote = response.context['quote']
        self.assertIsInstance(quote, Quote)

    def test_profile_page_has_rank_controls(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/alice/')
        self.assertIs(response.context['my_profile'], True)

    def test_user_page_has_no_rank_controls(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/bob/')
        self.assertIs(response.context['my_profile'], False)

    def test_bad_response_for_nonexistent_username(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/eve/')
        self.assertEqual(response.status_code, 404)


# class FunctionalTests(FunctionalTestCase):
#     fixtures = ['authors.json', 'quotes.json']
#     def setUp(self):
#         User.objects.create_user('alice', 'alice@gmail.com', 'pass1234')
#
#         if "TRAVIS" in environ:
#             username = environ["SAUCE_USERNAME"]
#             access_key = environ["SAUCE_ACCESS_KEY"]
#             # Create a desired capabilities object as a starting point.
#             capabilities = DesiredCapabilities.FIREFOX.copy()
#             capabilities['platform'] = "WINDOWS"
#             capabilities["tunnel-identifier"] = environ["TRAVIS_JOB_NUMBER"]
#             capabilities["build"] = environ["TRAVIS_BUILD_NUMBER"]
#             capabilities["tags"] = [environ["TRAVIS_PYTHON_VERSION"], "CI"]
#             hub_url = "%s:%s@localhost:4445" % (username, access_key)
#             self.selenium = webdriver.Remote(desired_capabilities=capabilities,
#                                              command_executor="http://%s/wd/hub" % hub_url)
#         else:
#             self.selenium = webdriver.Safari()
#             super(FunctionalTestCase, self).setUp()
#
#     def tearDown(self):
#         # QuoteRank.objects.all().delete()
#         # Profile.objects.all().delete()
#         # User.objects.all().delete()
#
#         self.selenium.quit()
#         super(FunctionalTestCase, self).tearDown()
# #
#    def test_like_button_home(self):
#        selenium = self.selenium
#        selenium.get('http://127.0.0.1:8000')
#
#        self.click_like_button()
#
#        self.assertIn('selected', like_button.get_attribute('class'))
#
#     def test_like_button_profile(self):
#         selenium = self.selenium
#         selenium.maximize_window()
#         self.signup()
#         wait = WebDriverWait(selenium, 10)
#         wait.until(lambda driver: 'alice' in driver.page_source)
#         selenium.get('http://127.0.0.1:8000/alice')
#         wait.until(lambda driver: driver.current_url == self.profile_url)
#         like_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, "like")))
#         like_button.click()
#         # wait.until(lambda driver: driver.current_url != self.profile_url)
#         self.assertIn('selected', like_button.get_attribute('class'))
#         self.assertTrue(like_button.get_attribute('disabled'))
