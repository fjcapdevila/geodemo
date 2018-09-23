from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Currency, Language, Provider, ServiceArea


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Providers."""

    class Meta:
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language', 'currency', 'service_areas')
        service_areas = serializers.PrimaryKeyRelatedField(
            many=True, queryset=ServiceArea.objects.all())


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
