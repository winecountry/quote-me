from django.contrib.auth.models import User
from django.test import TestCase

from daily_quote.models import Profile, Quote


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


class QuoteRecommendationTests(TestCase):
    fixtures = ['authors.json', 'quotes.json']
