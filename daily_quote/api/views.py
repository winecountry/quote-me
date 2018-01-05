from rest_framework import generics

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
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return Quote.recommend(profile)


class QuoteRankUpdate(generics.UpdateAPIView):
    queryset = QuoteRank.objects.all()
    serializer_class = QuoteRankSerializer

    def get_object(self):
        user = self.request.user
        quote_id = self.request.data['quote_id']
        return QuoteRank.objects.get(profile__user=user, quote__id=quote_id)

    def put(self, request, *args, **kwargs):
        print('UPDATE', self.request.data)
        user = self.request.user
        quote_id = self.request.data['quote_id']
        rank = self.request.data['rank']
        quoterank = QuoteRank.objects.get(profile__user=user, quote__id=quote_id)
        quoterank.rank = rank
        return self.update(request, *args, **kwargs)
