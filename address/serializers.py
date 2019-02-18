from address.models import UserAddress, GeoPointsText
from rest_framework import serializers


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = '__all__'


class GeoPointsTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoPointsText
        fields = '__all__'
