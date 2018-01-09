from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase


class LoginTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@gmail.com', 'test')

    def test_login(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        user = User.objects.get(username='test')
        self.assertEqual(response.context['user'], user)

    def test_logout(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.context['user'], AnonymousUser())
