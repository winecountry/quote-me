import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase

from daily_quote.models import Author, Quote
from quote_me.models import Profile


class DailyQuoteTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        create_quotes()
        create_users()

    def test_user_quote_rendered_to_home_page(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/')

        profile = Profile.objects.get(user__username='alice')
        quote = response.context['quote']

        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote.id, profile.current_quote_id)

    def test_user_quote_rendered_to_profile_page(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get('/alice/')

        profile = Profile.objects.get(user__username='alice')
        quote = response.context['quote']

        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote.id, profile.current_quote_id)

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


def create_quotes():
    with open('daily_quote/test.json') as authors:
        authors = json.load(authors)
        for author in authors:
            for quote in author['quotes']:
                Quote.objects.create(author=Author.objects.create(name=author['name'],
                                                                  profession=author['profession']),
                                     text=quote['quote_string'])


def create_users():
    User.objects.create_user('alice', 'alice@gmail.com', 'pass1234')
    User.objects.create_user('bob', 'bob@gmail.com', 'pass1234')
