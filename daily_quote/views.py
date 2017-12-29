from django.shortcuts import render
from .db_query import recommend_quote
from .db_seed import seed
from .models import User, Quote, Ranked


# Create your views here.
def index(req):
    # seed()
    user = User.objects.get(name="Alice")
    quote = recommend_quote(user)
    ctx = {
        'quote': quote
    }
    return render(req, 'daily_quote/index.html', ctx)
