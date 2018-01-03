from django.contrib.auth.models import User
from django.shortcuts import render

from quote_me.models import Profile
from .models import Quote


# Create your views here.
def index(request):
    return render(request, 'daily_quote/index.html', {})
