import datetime
from random import choice, randint

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    def recommend(profile):
        quote_id = profile.current_quote_id
        quoterank, _ = QuoteRank.objects.get_or_create(profile=profile, quote__id=quote_id)

        # if the user's current quote was recommended today, return the same quote
        if quoterank.date == datetime.date.today():
            return quoterank

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
            print("NO SIMILAR QUOTES: Defaulting to random quote...")
            quote = Quote.new_quote(profile)

        # create relationship between the user and quote
        QuoteRank.objects.create(profile=profile, quote=quote)

        return quoterank

    @staticmethod
    def random_quote():
        count = Quote.objects.count()
        pk = randint(1, count)
        return Quote.objects.get(pk=pk)

    @staticmethod
    def new_quote(profile):
        """
        Pick a new quote for a profile

        :param profile: profile to recommend to
        :return: a new quote the user has not seen
        """

        while True:
            quote = Quote.random_quote()
            if quote not in profile.quotes.values():
                return quote

    def __str__(self):
        return '"{}" - {}'.format(self.text, self.author.name)


class QuoteRank(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT)
    rank = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{} -> {} ({})".format(self.profile, self.quote, self.rank)


@receiver(post_save, sender=QuoteRank)
def update_current_quote(sender, instance, created, **kwargs):
    if created:
        profile = instance.profile
        quote = instance.quote
        profile.current_quote_id = quote.id
        profile.save()
