from django.db.models import Model, CharField, TextField, IntegerField, ManyToManyField, ForeignKey, PROTECT
from django.contrib.auth.models import AbstractUser


class Quote(Model):
    author = CharField(max_length=45)
    # profession = CharField(max_length=45)
    text = TextField()

    def __str__(self):
        return '"{}" - {}'.format(self.text, self.author)


class User(AbstractUser):
    quotes = ManyToManyField(Quote, through='Ranked')

    def __str__(self):
        return self.username


class Ranked(Model):
    user = ForeignKey(User, on_delete=PROTECT)
    quote = ForeignKey(Quote, on_delete=PROTECT)
    rank = IntegerField()

    def __str__(self):
        return "{} -> {} ({})".format(self.user, self.quote, self.rank)
