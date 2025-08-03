from rest_framework import serializers
from .models import PriceData


class PriceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceData
        fields = '__all__'