from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, TransactionTestCase

from daily_quote.models import Author, Quote


class LoginTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': 'test',
        }
        User.objects.create_user(**self.credentials)
        author = Author.objects.create(name="John Smith", profession="Farmer")
        Quote.objects.create(text="I like chicken", author=author)

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


class SignupTests(TransactionTestCase):
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
