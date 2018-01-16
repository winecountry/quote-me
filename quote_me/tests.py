from django.contrib.auth.models import AnonymousUser, User
from django.test import LiveServerTestCase, TestCase, TransactionTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import environ

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from daily_quote.models import Author, Quote


class LoginTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        author = Author.objects.create(name='John Smith', profession='Farmer')
        Quote.objects.create(text='I like chicken', author=author)

        self.credentials = {
            'username': 'test',
            'password': 'test',
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/login/', self.credentials, follow=True)
        user = User.objects.get(username='test')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.context['user'], user)

    def test_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        user = User.objects.get(username='test')
        self.assertEqual(response.context['user'], user)
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.context['user'], AnonymousUser())


class SignupTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.credentials = {
            'username': 'test2',
            'first_name': 'test2',
            'last_name': 'test2',
            'email': 'test2@test.com',
            'password1': 'thisisatest',
            'password2': 'thisisatest',
        }
        author = Author.objects.create(name='John Smith', profession='Farmer')
        Quote.objects.create(text='I like chicken', author=author)

    def test_signup(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/signup/', self.credentials, follow=True)
        user = User.objects.get(username='test2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.context['user'], user)


class FunctionalTests(FunctionalTestCase):
    def test_like_button_profile(self):
        selenium = self.selenium
        selenium.maximize_window()
        self.signup()
        wait = WebDriverWait(selenium, 10)
        wait.until(lambda driver: 'alice' in driver.page_source)
        selenium.get('http://127.0.0.1:8000/alice')
        wait.until(lambda driver: driver.current_url == self.profile_url)
        like_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, "like")))
        like_button.click()
        # wait.until(lambda driver: driver.current_url != self.profile_url)
        self.assertIn('selected', like_button.get_attribute('class'))
        self.assertTrue(like_button.get_attribute('disabled'))
