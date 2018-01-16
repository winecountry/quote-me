from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^like/$', views.rank_quote, {'rank': 1}, name='like_quote'),
    url(r'^dislike/$', views.rank_quote, {'rank': -1}, name='dislike_quote'),
    url(r'^(?P<username>.+)/$', views.user_profile, name='profile'),
]
