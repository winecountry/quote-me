from django.contrib.auth.models import AnonymousUser, User
from django.test import LiveServerTestCase, TestCase, TransactionTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import environ

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


class FunctionalTestCase(LiveServerTestCase):

    def setUp(self):
        if "TRAVIS" in environ:
            username = environ["SAUCE_USERNAME"]
            access_key = environ["SAUCE_ACCESS_KEY"]
            # Create a desired capabilities object as a starting point.
            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities['platform'] = "WINDOWS"
            capabilities["tunnel-identifier"] = environ["TRAVIS_JOB_NUMBER"]
            capabilities["build"] = environ["TRAVIS_BUILD_NUMBER"]
            capabilities["tags"] = [environ["TRAVIS_PYTHON_VERSION"], "CI"]
            hub_url = "%s:%s@localhost:4445" % (username, access_key)
            self.selenium = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s/wd/hub" % hub_url)
        else:
            self.selenium = webdriver.Safari()
            super(FunctionalTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(FunctionalTestCase, self).tearDown()

    def test(self):
        assert True

#    def test_page_load(self):
#        selenium = self.selenium
#        selenium.get('http://localhost:8000')
#
#        assert "No results found." not in selenium.page_source

#    def test_register(self):
#        selenium = self.selenium
#        selenium.get('http://127.0.0.1:8000/signup/')
#        first_name = selenium.find_element_by_id('id_first_name')
#        last_name = selenium.find_element_by_id('id_last_name')
#        username = selenium.find_element_by_id('id_username')
#        email = selenium.find_element_by_id('id_email')
#        password1 = selenium.find_element_by_id('id_password1')
#        password2 = selenium.find_element_by_id('id_password2')
#
#        submit = selenium.find_element_by_name()
