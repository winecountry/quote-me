from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from daily_quote.models import Quote
from .forms import SignUpForm


def home(request):
    if request.user.is_authenticated:
        quote = request.user.profile.recommend().quote
    else:
        quote = Quote.random_quote()

    return render(request, 'quote_me/home.html', {'quote': quote})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignUpForm()
    return render(request, 'quote_me/signup.html', {'form': form})
