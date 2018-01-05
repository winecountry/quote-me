from random import choice, choices, randint

from django.contrib.auth.models import User

from quote_me.models import Profile
from .models import Author, Quote, QuoteRank


def get_quotes():
    import json
    from daily_quote.models import Quote

    with open('data/quotes.json', 'r') as data:
        quotes = []
        data_json = json.loads(data.read())
        for author_obj in data_json:
            author = Author.objects.create(name=author_obj['name'], profession=author_obj['profession'])
            print(author.name)
            for quote_obj in author_obj['quotes']:
                print('.', end='')
                quotes.append(Quote.objects.create(author=author, text=quote_obj['quote_string']))
            print()
        return quotes


def inject_failure():
    author = {
        'name': 'Tony Hoare',
        'profession': 'Programmer'
    }
    quote = {
        'text': "This has led to innumerable errors, vulnerabilities, and system crashes."
    }
    tony = Author.objects.create(**author)
    Quote.objects.create(author=tony, **quote)


def seed(with_quotes=False):
    """
    https://stackoverflow.com/questions/33259477/table-was-deleted-how-can-i-make-django-recreate-it
    :return:
    """

    # clear all users and quotes
    QuoteRank.objects.all().delete()
    Profile.objects.all().delete()
    if with_quotes:
        Quote.objects.all().delete()
        inject_failure()

    users = ['Alice', 'Bob', 'Eve', 'John', 'Paul', 'George', 'Ringo', 'Pete', 'Rathgar', 'Steve', 'Robert']
    quotes = get_quotes() if with_quotes else Quote.objects.all()
    ranks = [-1, 0, 1]
    profiles = []
    for username in users:
        user, _ = User.objects.get_or_create(username=username)
        profile, _ = Profile.objects.get_or_create(user=user)
        profiles.append(profile)
    for profile in profiles:
        for quote in choices(quotes, k=randint(1, 2000)):
            QuoteRank.objects.create(profile=profile, quote=quote, rank=choice(ranks))
