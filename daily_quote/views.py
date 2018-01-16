from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

#from daily_quote.forms import ProfileEditForm, UserEditForm
from daily_quote.models import Profile


def user_profile(request, username):
    context = {
        'my_profile': False,
    }

    try:
        if request.user.username == username:
            context['my_profile'] = True
            profile = request.user.profile


#            if request.method == 'POST':
#                user_edit_form = UserEditForm(request.POST, instance=request.user)
#                profile_edit_form = ProfileEditForm(request.POST, instance=request.user.profile)
#                
#                if all(user_edit_form.is_valid(), profile_edit_form.is_valid()):
#                    user = user_edit_form.save()
#                    profile = profile_edit_form.save()
        else:
#            user_edit_form = UserEditForm(instance=request.user)
#            profile_edit_form = ProfileEditForm(instance=request.user.profile)
            profile = Profile.objects.get(user__username=username)
#
#        context['user_edit_form'] = user_edit_form
#        context['profile_edit_form'] = profile_edit_form

        quoterank = profile.recommend()

        context['quote'] = quoterank.quote
        context['rank'] = quoterank.rank

    except Profile.DoesNotExist:
        raise Http404("Profile Does Not Exist")

    return render(request, 'daily_quote/profile.html', context)
