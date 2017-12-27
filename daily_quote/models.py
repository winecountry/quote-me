from django.db.models import Model, CharField, TextField, ManyToManyField, ForeignKey


class User(Model):
    name = CharField(max_length=30)
    # password = CharField(max_length=50)
    # salt = CharField(max_length=10)
    quotes = ManyToManyField('Quote', through='Ranked')


class Quote(Model):
    author = CharField(max_length=45)
    # profession = CharField(max_length=45)
    text = TextField()


class Ranked(Model):
    user = ForeignKey(User)
    quote = ForeignKey(Quote)
    rank = 0
