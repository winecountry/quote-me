from random import choice, choices, randint

from django.contrib.auth.models import User

from daily_quote.stock_users import stock_users
from quote_me.models import Profile
from .models import Author, Quote, QuoteRank

"""
FOR DEVELOPMENT PURPOSES ONLY
Run `seed()` once after migrating changes to the database
"""


def get_quotes():
    """
    Parse JSON data into Model objects

    :return: List of Quote Model objects
    """
    import json
    from daily_quote.models import Quote

    with open('data/quotes.json', 'r') as data:
        quotes = []
        author_list = json.loads(data.read())
        for author_obj in author_list:
            author, _ = Author.objects.get_or_create(name=author_obj['name'], profession=author_obj['profession'])
            print(author.name)
            for quote_obj in author_obj['quotes']:
                print('.', end='')
                quote, _ = Quote.objects.get_or_create(author=author, text=quote_obj['quote_string'])
                quotes.append(quote)
            print()
        return quotes


def inject_failure():
    """
    undefined is not a function
    """

    author = {
        'name': 'Tony Hoare',
        'profession': 'Programmer'
    }

    quote = {
        'text': "This has led to innumerable errors, vulnerabilities, and system crashes."
    }

    Quote.objects.create(author=Author.objects.create(**author), **quote)


def seed(with_quotes=True):
    """
    https://stackoverflow.com/questions/33259477/table-was-deleted-how-can-i-make-django-recreate-it
    :return:
    """

    if with_quotes:
        inject_failure()

    # build Model objects
    users = stock_users
    quotes = get_quotes() if with_quotes else Quote.objects.all()
    ranks = [-1, 0, 1]
    profiles = []
    for user_obj in users:
        user, _ = User.objects.get_or_create(**user_obj, password='pass1234')
        profile, _ = Profile.objects.get_or_create(user=user)
        profiles.append(profile)
    for profile in profiles:
        for quote in choices(quotes, k=randint(1, 2000)):
            QuoteRank.objects.create(profile=profile, quote=quote, rank=choice(ranks))
