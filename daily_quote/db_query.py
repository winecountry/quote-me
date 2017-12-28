from random import choice
from .models import User, Quote


def recommend_quote(user):
    # Pick a random quote the user likes
    quote = choice(Quote.objects.filter(ranked__user=user, ranked__rank=1))
    # Find other users who like that quote
    users = User.objects.filter(ranked__quote_id=quote.id, ranked__rank=1).exclude(id=user.id)
    # Find other quotes those users like
    quotes = Quote.objects.filter(user__in=users, ranked__rank=1).distinct().exclude(id=quote.id)
    # Return one at random
    return choice(quotes)
