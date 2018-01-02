from django.shortcuts import render
from django.http import HttpResponseRedirect

from .db_query import recommend_quote
from .db_seed import seed
from .models import User, Quote, Ranked


# Create your views here.
def index(req):
    user = User.objects.get(username="Alice")
    quote = recommend_quote(user)
    ctx = {
        'quote': quote
    }
    return render(req, 'daily_quote/index.html', ctx)

def login(req):
    # process the form data for POST requests
    if req.method == 'POST':
        # create a form instance an populate it with data from the request:
        form = LoginForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # TODO: process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(req, 'login.html', {'form': form})
