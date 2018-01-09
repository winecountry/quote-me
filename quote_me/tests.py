from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, TransactionTestCase

from daily_quote.models import Author, Quote


class LoginTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        author = Author.objects.create(name="John Smith", profession="Farmer")
        Quote.objects.create(text="I like chicken", author=author)
        User.objects.create_user('test', 'test@gmail.com', 'test')

    def test_login(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        user = User.objects.get(username='test')
        self.assertEqual(response.context['user'], user)

    def test_logout(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.context['user'], AnonymousUser())
