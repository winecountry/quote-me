import datetime
from django.shortcuts import render

from daily_quote.models import Quote, QuoteRank
from quote_me.models import Profile


def daily_quote(request, username):
    my_profile = False
    rank = 0

    try:
        if username == 'me':
            profile = Profile.objects.get(user=request.user)
            my_profile = True
        else:
            profile = Profile.objects.get(user__username=username)
            if request.user.username == username:
                my_profile = True

        try:
            quoterank = QuoteRank.objects.get(profile=profile, quote__id=profile.current_quote_id)
            rank = quoterank.rank

            # return the current quote if it was recommended today, otherwise recommend a new quote
            quote = quoterank.quote if quoterank.date == datetime.date.today() else Quote.recommend(profile)

        except QuoteRank.DoesNotExist:
            quote = Quote.recommend(profile)

    except Profile.DoesNotExist:
        quote = Quote.recommend()

    context = {
        'quote': quote,
        'my_profile': my_profile,
        'rank': rank,
    }

    return render(request, 'daily_quote/index.html', context)
