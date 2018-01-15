from django.http import Http404
from django.shortcuts import render

from daily_quote.models import Profile, Quote


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

        context['profile'] = profile
        context['quote'] = quoterank.quote
        context['rank'] = quoterank.rank

    except Profile.DoesNotExist:
        raise Http404("Profile Does Not Exist")

    return render(request, 'daily_quote/profile.html', context)


def home(request):
    if request.user.is_authenticated:
        quote = request.user.profile.recommend().quote
    else:
        quote = Quote.random_quote()

    context = {
        'current_route': 'home',
        'quote': quote
    }

    return render(request, 'daily_quote/home.html', context)
