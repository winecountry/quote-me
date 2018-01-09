from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quotes = models.ManyToManyField('daily_quote.Quote', through='daily_quote.QuoteRank')
    current_quote_id = models.IntegerField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    from daily_quote.models import Quote
    from daily_quote.models import QuoteRank

    if created:
        profile = Profile.objects.create(user=instance)
        QuoteRank.objects.create(profile=profile, quote=Quote.random_quote())
    instance.profile.save()
