from rest_framework.serializers import ModelSerializer

from daily_quote.models import Quote


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'
