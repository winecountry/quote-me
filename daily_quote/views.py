from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Quote


# Create your views here.
def index(req):
    user = User.objects.get(username="Alice")
    ctx = {
        'quote': Quote.recommend(user)
    }
    return render(req, 'daily_quote/index.html', ctx)
