from django.http import Http404
from django.shortcuts import render

from daily_quote.models import Quote, QuoteRank
from quote_me.models import Profile


def user_profile(request, username):
    context = {
        'my_profile': False,
    }

    try:
        profile = Profile.objects.get(user__username=username)
        if request.user.username == username:
            context['my_profile'] = True

        quoterank = Quote.recommend(profile)

        context['quote'] = quoterank.quote
        context['rank'] = quoterank.rank

    except Profile.DoesNotExist:
        raise Http404("Profile Does Not Exist")

    return render(request, 'daily_quote/profile.html', context)
