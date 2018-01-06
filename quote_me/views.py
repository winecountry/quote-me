from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from daily_quote.db_seed import seed
from quote_me.models import Profile
from .forms import SignUpForm


def home(request):
    return render(request, 'quote_me/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Profile.objects.get_or_create(user=user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignUpForm()
    return render(request, 'quote_me/signup.html', {'form': form})
