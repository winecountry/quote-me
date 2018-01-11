from django.http import Http404
from django.shortcuts import render

from daily_quote.models import Profile


def user_profile(request, username):
    context = {
        'current_route': 'profile',
        'my_profile': False,
    }

    try:
        if request.user.username == username:
            context['my_profile'] = True
            profile = request.user.profile
        else:
            profile = Profile.objects.get(user__username=username)

        quoterank = profile.recommend()

        context['quote'] = quoterank.quote
        context['rank'] = quoterank.rank

    except Profile.DoesNotExist:
        raise Http404("Profile Does Not Exist")

    return render(request, 'daily_quote/profile.html', context)
