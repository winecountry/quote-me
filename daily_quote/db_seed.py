from random import choice, choices, randint
from .models import User, Quote, Ranked


def create_user(name):
    user = User(name=name)
    user.save()
    return user


def create_quote(author, text):
    quote = Quote(author=author, text=text)
    quote.save()
    return quote


def create_ranked(user, quote, rank=0):
    ranked = Ranked(user=user, quote=quote, rank=rank)
    ranked.save()
    return ranked


def seed():
    Ranked.objects.all().delete()
    User.objects.all().delete()
    Quote.objects.all().delete()
    users = ['Alice', 'Bob', 'Eve', 'John', 'Paul', 'George', 'Ringo']
    author = ['Gary S.', 'Jim W.', 'Taylor A.', 'Jerry M.', 'Tim Q.',
              'Tony H.', 'Joe S.', 'Ben G.', 'Chris P.', 'Larry N.']
    texts = ['Quote 1', 'Quote 2', 'Quote 3', 'Quote 4', 'Quote 5',
             'Quote 6', 'Quote 7', 'Quote 8', 'Quote 9', 'Quote 10']
    ranks = [-1, 0, 1]
    users = map(create_user, users)
    quotes = list(map(lambda t: create_quote(t[0], t[1]), zip(author, texts)))
    for user in users:
        for quote in choices(quotes, k=randint(0, 8)):
            create_ranked(user, quote, rank=choice(ranks))
