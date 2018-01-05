from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    url(r'^(?P<username>.+)/$', views.user_home),
]
