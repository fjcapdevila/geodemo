from rest_framework import serializers

from .models import Currency, Language, Provider, ServiceArea


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Providers."""

    class Meta:
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language', 'currency', 'service_areas')
        service_areas = serializers.PrimaryKeyRelatedField(
            many=True, queryset=ServiceArea.objects.all())


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Languages."""

    class Meta:
        model = Language
        fields = ('name', )


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Currencies."""

    class Meta:
        model = Currency
        fields = ('name', )


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Service Areas."""

    class Meta:
        model = ServiceArea
        fields = ('name', 'provider', 'area')
