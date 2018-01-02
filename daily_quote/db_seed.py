from random import choice, choices, randint

from django.contrib.auth.models import User

from quote_me.models import Profile
from .models import Author, Quote, QuoteRank


def create_user(username):
    user = User(username=username)
    user.save()
    return user


def create_profile(user):
    profile = Profile(user=user)
    profile.save()
    return profile


def create_quote(author, text):
    quote = Quote(author=author, text=text)
    quote.save()
    return quote


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
                quote = Quote(author=author, text=quote_obj['quote_string'])
                quote.save()
                quotes.append(quote)
            print()
        return quotes


def inject_failure():
    tony = Author.objects.create(name='Tony Hoare', profession='Programmer')
    Quote(author=tony, text="This has led to innumerable errors, vulnerabilities, and system crashes.").save()


def create_ranked(profile, quote, rank=0):
    ranked = QuoteRank(profile=profile, quote=quote, rank=rank)
    ranked.save()
    return ranked


def seed(with_quotes=False):
    """
    https://stackoverflow.com/questions/33259477/table-was-deleted-how-can-i-make-django-recreate-it
    :return:
    """

    # clear all users and quotes
    QuoteRank.objects.all().delete()
    User.objects.all().delete()
    if with_quotes:
        Quote.objects.all().delete()
        inject_failure()

    users = ['Alice', 'Bob', 'Eve', 'John', 'Paul', 'George', 'Ringo', 'Pete', 'Rathgar', 'Steve', 'Robert']
    quotes = get_quotes() if with_quotes else Quote.objects.all()
    ranks = [-1, 0, 1]
    for user in map(create_profile, [create_user(user) for user in users]):
        for quote in choices(quotes, k=randint(1, 2000)):
            create_ranked(user, quote, rank=choice(ranks))
