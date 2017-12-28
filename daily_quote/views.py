import os
from django.shortcuts import render
from .db_query import recommend_quote
from .models import User, Quote, Ranked
from django.http import HttpResponse


# Create your views here.
def index(req):
    user = User.objects.get(name="Eve")
    quote = recommend_quote(user)
    ctx = {
        'os': os,
        'quote': quote
    }
    return render(req, 'daily_quote/index.html', ctx)
