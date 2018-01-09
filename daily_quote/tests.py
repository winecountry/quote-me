from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, TransactionTestCase

from daily_quote.models import Author, Quote
from quote_me.models import Profile


class DailyQuoteTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        author = Author.objects.create(name="John Smith", profession="Farmer")
        Quote.objects.create(text="I like chicken", author=author)
        User.objects.create_user('test', 'test@gmail.com', 'test')

    def test_user_quote_rendered_to_profile_page(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/test/')

        profile = Profile.objects.get(user__username='test')
        quote = response.context['quote']

        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote.id, profile.current_quote_id)

    def test_profile_page_has_like_controls(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/test/')
        self.assertIs(response.context['my_profile'], True)

    def test_user_page_has_no_like_controls(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/other/')
        self.assertIs(response.context['my_profile'], False)
