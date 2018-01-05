import datetime
from django.shortcuts import render

from daily_quote.models import Quote, QuoteRank
from quote_me.models import Profile


def user_home(request, username):
    try:
        if username == 'me':
            profile = Profile.objects.get(user=request.user)
        else:
            profile = Profile.objects.get(user__username=username)

        try:
            quoterank = QuoteRank.objects.get(profile=profile, quote__id=profile.current_quote_id)

            # return the current quote if it was recommended today, otherwise recommend a new quote
            quote = quoterank.quote if quoterank.date == datetime.date.today() else Quote.recommend(profile).quote

        except QuoteRank.DoesNotExist:
            quote = Quote.recommend(profile).quote

    except Profile.DoesNotExist:
        quote = Quote.recommend().quote

    context = {
        'quote_text': quote.text,
        'author': quote.author
    }

    return render(request, 'daily_quote/index.html', context)
