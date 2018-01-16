from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class FunctionalTestCase(LiveServerTestCase):
    fixtures = ['authors.json', 'quotes.json']

    signup_url = 'http://127.0.0.1:8000/signup/'
    profile_url = 'http://127.0.0.1:8000/alice/'
    home_url = 'http://127.0.0.1:8000/'
    login_url = 'http://127.0.0.1:8000/login/'
    logout_url = 'http://127.0.0.1:8000/logout/'

    def setUp(self):
        User.objects.create_user('alice', 'alice@gmail.com', 'pass1234')

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
            self.selenium = webdriver.Remote(desired_capabilities=capabilities,
                                             command_executor="http://%s/wd/hub" % hub_url)
        else:
            self.selenium = webdriver.Safari()
            super(FunctionalTestCase, self).setUp()

    def tearDown(self):
        # QuoteRank.objects.all().delete()
        # Profile.objects.all().delete()
        # User.objects.all().delete()

        self.selenium.quit()
        super(FunctionalTestCase, self).tearDown()

    def signup(self):
        selenium = self.selenium
        selenium.get(self.signup_url)

        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        first_name.send_keys('alice')
        username.send_keys('alice')
        email.send_keys('alice@gmail.com')
        password1.send_keys('pass1234')
        password2.send_keys('pass1234')

        selenium.find_element_by_id('submit-button').click()

    def login(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/login/')

        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')

        username.send_keys('alice')
        password.send_keys('pass1234')

        selenium.find_element_by_id('submit-button').click()
