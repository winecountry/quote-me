from django.db.models import Model, CharField, TextField, IntegerField, ManyToManyField, ForeignKey


class Quote(Model):
    author = CharField(max_length=45)
    # profession = CharField(max_length=45)
    text = TextField()

    def __str__(self):
        return '"{}" - {}'.format(self.text, self.author)


class User(Model):
    name = CharField(max_length=30)
    # password = CharField(max_length=50)
    # salt = CharField(max_length=10)
    quotes = ManyToManyField(Quote, through='Ranked')

    def __str__(self):
        return self.name


class Ranked(Model):
    user = ForeignKey(User)
    quote = ForeignKey(Quote)
    rank = IntegerField()

    def __str__(self):
        return "{} -> {} ({})".format(self.user, self.quote, self.rank)
