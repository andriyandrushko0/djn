from rest_framework import serializers

from .models import CoinRequest, CoinResponse


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinRequest
        fields = "__all__"


class ResponseSerializer(serializers.ModelSerializer):
    coin_request = RequestSerializer()

    class Meta:
        model = CoinResponse
        fields = ("id", "denomination", "year", "date_time", "coin_request")
