from random import choice, choices, randint
from .models import User, Quote, Ranked


def create_user(username):
    user = User(username=username)
    user.save()
    return user


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
        for author in data_json:
            print(author['name'])
            for quote_obj in author['quotes']:
                print('.', end='')
                quote = Quote(author=author['name'], text=quote_obj['quote_string'])
                quote.save()
                quotes.append(quote)
            print()
        return quotes


def inject_failure():
    Quote(author='Tony Hoare', text="This has led to innumerable errors, vulnerabilities, and system crashes.").save()


def create_ranked(user, quote, rank=0):
    ranked = Ranked(user=user, quote=quote, rank=rank)
    ranked.save()
    return ranked


def seed():
    """
    https://stackoverflow.com/questions/33259477/table-was-deleted-how-can-i-make-django-recreate-it
    :return:
    """

    # clear all users and quotes
    Ranked.objects.all().delete()
    User.objects.all().delete()
    # Quote.objects.all().delete()

    users = ['Alice', 'Bob', 'Eve', 'John', 'Paul', 'George', 'Ringo', 'Pete', 'Rathgar', 'Steve', 'Robert']
    quotes = Quote.objects.all()
    ranks = [-1, 0, 1]
    for user in map(create_user, users):
        for quote in choices(quotes, k=randint(1, 2000)):
            create_ranked(user, quote, rank=choice(ranks))

    # inject_failure()
