from random import choice, randint

from django.db import models

from quote_me.models import Profile


class Author(models.Model):
    name = models.CharField(max_length=45)
    profession = models.CharField(max_length=45)


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    text = models.TextField()

    @staticmethod
    def recommend(user=None):
        return recommend_quote(user)

    def __str__(self):
        return '"{}" - {}'.format(self.text, self.author)


class QuoteRank(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT)
    rank = models.IntegerField()

    def __str__(self):
        return "{} -> {} ({})".format(self.profile, self.quote, self.rank)


def random_row():
    count = Quote.objects.all().count()
    pk = randint(1, count)
    return Quote.objects.get(pk=pk)


def recommend_quote(user):
    if user is None:
        print("NO USER SPECIFIED: Defaulting to random selection...")
        return random_row()

    try:
        # Get all quotes the user likes
        user_quotes = Quote.objects.filter(profile__user=user)
        user_liked_quotes = user_quotes.filter(quoterank__rank=1)
        # Pick a random quote the user likes
        quote = choice(user_liked_quotes)
        # Find other users who like that quote
        users = Profile.objects.filter(quoterank__quote=quote, quoterank__rank=1).exclude(user=user)
        # Find other quotes those users like (excluding quotes the user has already seen)
        quotes = Quote.objects.filter(profile__user__in=users, quoterank__rank=1).distinct()\
                              .exclude(id=quote.id, profile__user__quotes=user_quotes)
        # Return one at random
        return choice(quotes)
    except IndexError:
        print("NO SIMILAR QUOTES FOUND: Defaulting to random selection...", random_row())
        return random_row()

