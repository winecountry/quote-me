from rest_framework import generics

from daily_quote.api.serializers import QuoteSerializer
from daily_quote.models import Quote


class QuoteDetail(generics.RetrieveAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
