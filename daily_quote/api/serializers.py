from rest_framework import serializers

from daily_quote.models import Quote, Author, QuoteRank


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    serializer_related_field = AuthorSerializer

    class Meta:
        model = Quote
        fields = '__all__'

        depth = 1


class QuoteRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRank
        fields = '__all__'
        extra_kwargs = {
            'profile': {'required': False},
            'quote': {'required': False},
        }
