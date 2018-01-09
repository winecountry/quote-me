import datetime
from random import choice, randint

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    name = models.CharField(max_length=45)
    profession = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    text = models.TextField()

    @staticmethod
    def random_quote():
        count = Quote.objects.count()
        pk = randint(1, count)
        return Quote.objects.get(pk=pk)

    def __str__(self):
        return '"{}" - {}'.format(self.text, self.author.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quotes = models.ManyToManyField(Quote, through='daily_quote.QuoteRank')
    current_quote = models.ForeignKey(Quote, related_name='current_quote', null=True, on_delete=models.PROTECT)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def recommend(self):
        quote = self.current_quote
        quoterank, _ = QuoteRank.objects.get_or_create(profile=self, quote=quote)

        # if the user's current quote was recommended today, return the same quote
        if quoterank.date == datetime.date.today():
            return quoterank

        try:
            # Get all quotes the user likes
            profile_quotes = Quote.objects.filter(profile=self)
            profile_liked_quotes = profile_quotes.filter(quoterank__rank=1)

            # Pick a random quote the user likes
            quote = choice(profile_liked_quotes)

            # Find other users who like that quote
            profiles = Profile.objects.filter(quoterank__quote=quote, quoterank__rank=1).exclude(id=self.id)

            # Find other quotes those users like (excluding quotes the user has already seen)
            quotes = Quote.objects.filter(profile__in=profiles, quoterank__rank=1).distinct()\
                                  .exclude(id=quote.id, profile__quotes=profile_quotes)

            # Return one at random
            quote = choice(quotes)
        except IndexError:
            print("NO SIMILAR QUOTES: Defaulting to random quote...")
            quote = self.new_quote()

        # create relationship between the user and quote
        QuoteRank.objects.create(profile=self, quote=quote)

        return quoterank

    def new_quote(self):
        """
        Pick a new quote for a profile

        :return: a new quote the user has not seen
        """

        while True:
            quote = Quote.random_quote()
            if quote not in self.quotes.values():
                return quote

    def __str__(self):
        return str(self.user)


class QuoteRank(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT)
    rank = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{} -> {} ({})".format(self.profile, self.quote, self.rank)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        QuoteRank.objects.create(profile=profile, quote=Quote.random_quote())
    instance.profile.save()


@receiver(post_save, sender=QuoteRank)
def update_current_quote(sender, instance, created, **kwargs):
    if created:
        profile = instance.profile
        quote = instance.quote
        profile.current_quote = quote
        profile.save()
