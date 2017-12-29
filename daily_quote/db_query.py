from random import choice, randint
from .models import User, Quote


def random_row():
    count = Quote.objects.all().count()
    pk = randint(1, count)
    return Quote.objects.get(pk=pk)


def recommend_quote(user):
    try:
        # Pick a random quote the user likes
        quote = choice(Quote.objects.filter(ranked__user=user, ranked__rank=1))
        # Find other users who like that quote
        users = User.objects.filter(ranked__quote_id=quote.id, ranked__rank=1).exclude(id=user.id)
        # Find other quotes those users like (excluding quotes already seen)
        user_quotes = Quote.objects.filter(ranked__user=user)
        quotes = Quote.objects.filter(user__in=users, ranked__rank=1).distinct()\
                              .exclude(id=quote.id, user__quotes=user_quotes)
        # Return one at random
        return choice(quotes)
    except IndexError:
        print("NO SIMILAR QUOTES FOUND: Defaulting to random selection...")
        return random_row()
