from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import QuoteDetail, QuoteRecommend, QuoteRankUpdate

urlpatterns = [
    url(r'^recommend', QuoteRecommend.as_view()),
    url(r'^quotes/(?P<pk>[0-9]+)/$', QuoteDetail.as_view()),
    url(r'^quoterank', QuoteRankUpdate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
