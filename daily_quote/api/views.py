from rest_framework import generics
from rest_framework.response import Response

from daily_quote.api.serializers import QuoteSerializer, QuoteRankSerializer
from daily_quote.models import Quote, QuoteRank


class QuoteDetail(generics.RetrieveAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteRecommend(generics.RetrieveAPIView):
    queryset = QuoteRank.objects.all()
    serializer_class = QuoteRankSerializer

    def get_object(self):
        return self.request.user.profile.recommend()


class QuoteRankUpdate(generics.UpdateAPIView):
    queryset = QuoteRank.objects.all()
    serializer_class = QuoteRankSerializer

    def get_object(self):
        # print("============================START============================")
        # print("REQUEST", self.request.__dict__)
        # print("DJANGO REQUEST", self.request.authenticators[1].__dict__)
        # print("AUTHENTICATORS", self.request.authenticators)
        # print("  SESSION", self.request.authenticators[0].__dict__)
        # print("  BASIC", self.request.authenticators[1].__dict__)
        # print("=============================END=============================")
        user = self.request.user
        quote = user.profile.current_quote
        return QuoteRank.objects.get(profile__user=user, quote=quote)

    # def put(self, request, *args, **kwargs):
    #     # default database update
    #     self.update(request, *args, **kwargs)
    #
    #     # Return JSON data
    #     serializer = self.serializer_class(self.get_object())
    #     return Response(serializer.data)
