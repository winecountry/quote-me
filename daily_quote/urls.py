from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^(?P<username>.+)/$', views.daily_quote),
]
