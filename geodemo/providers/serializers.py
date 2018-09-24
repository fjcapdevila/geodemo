from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Currency, Language, Provider, ServiceArea


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Providers."""

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language', 'currency', 'service_areas',
                  'owner')


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Languages."""

    class Meta:
        model = Language
        fields = ('name', )


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currencies."""

    class Meta:
        model = Currency
        fields = ('name', )


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    """Serializer for Service Areas."""

    class Meta:
        model = ServiceArea
        geo_field = "area"
        fields = '__all__'


class CoordinateSerializer(serializers.Serializer):
    """Serializer to validate latitud and longitude values."""
    lat = serializers.FloatField(min_value=-90.0, max_value=90.0)
    lng = serializers.FloatField(min_value=-180.0, max_value=180.0)
