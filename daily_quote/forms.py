from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User

from daily_quote.models import Profile

class UserEditForm(ModelForm):
#    username = forms.CharField(required=True)
#    email = forms.EmailField(required=True)
#    first_name = forms.CharField(required=False)
#    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'birth_date', 'bio']
