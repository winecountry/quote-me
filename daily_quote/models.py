import datetime
from random import choice, randint

from django.db import models

from quote_me.models import Profile


class Author(models.Model):
    name = models.CharField(max_length=45)
    profession = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    text = models.TextField()

    @staticmethod
    def recommend(profile=None):
        quote = recommend_quote(profile)
        quoterank, _ = QuoteRank.objects.get_or_create(profile=profile, quote=quote, rank=0)
        return quoterank

    def __str__(self):
        return '"{}" - {}'.format(self.text, self.author.name)


class QuoteRank(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT)
    rank = models.IntegerField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{} -> {} ({})".format(self.profile, self.quote, self.rank)


def random_quote():
    count = Quote.objects.all().count()
    pk = randint(1, count)
    return Quote.objects.get(pk=pk)


def recommend_quote(profile):
    if profile is None:
        print("NO PROFILE SPECIFIED: Defaulting to random selection...")
        return random_quote()

    try:
        # Get all quotes the user likes
        profile_quotes = Quote.objects.filter(profile=profile)
        profile_liked_quotes = profile_quotes.filter(quoterank__rank=1)

        # Pick a random quote the user likes
        quote = choice(profile_liked_quotes)

        # Find other users who like that quote
        profiles = Profile.objects.filter(quoterank__quote=quote, quoterank__rank=1).exclude(id=profile.id)

        # Find other quotes those users like (excluding quotes the user has already seen)
        quotes = Quote.objects.filter(profile__in=profiles, quoterank__rank=1).distinct()\
                              .exclude(id=quote.id, profile__quotes=profile_quotes)

        # Return one at random
        quote = choice(quotes)
    except IndexError:
        quote = random_quote()
        print("NO SIMILAR QUOTES FOUND: Defaulting to random selection...", quote)

    # Update last recommended quote
    profile.current_quote_id = quote.id
    profile.save()

    return quote

