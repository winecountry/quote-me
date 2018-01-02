from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm
#from daily_quote import views 

def index(request):
    return redirect('signup/')

def home(request):
    pass

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('daily_quote/index')
    else:
        form = SignUpForm()
    return render(request, 'quote_me/signup.html', {'form': form})

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
