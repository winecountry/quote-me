from rest_framework import generics
from rest_framework.response import Response

from daily_quote.api.serializers import QuoteSerializer, QuoteRankSerializer
from daily_quote.models import Quote, QuoteRank
from quote_me.models import Profile


class QuoteDetail(generics.RetrieveAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteRecommend(generics.RetrieveAPIView):
    queryset = QuoteRank.objects.all()
    serializer_class = QuoteRankSerializer

    def get_object(self):
        return Quote.recommend(self.request.user.profile)


class QuoteRankUpdate(generics.UpdateAPIView):
    queryset = QuoteRank.objects.all()
    serializer_class = QuoteRankSerializer

    def get_object(self):
        user = self.request.user
        quote_id = user.profile.current_quote_id
        return QuoteRank.objects.get(profile__user=user, quote__id=quote_id)

    def put(self, request, *args, **kwargs):
        # default database update
        self.update(request, *args, **kwargs)

        # Return JSON data
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data)
