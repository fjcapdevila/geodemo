from rest_framework import viewsets

from .models import Provider, Language, Currency, ServiceArea
from .serializers import ProviderSerializer, LanguageSerializer, CurrencySerializer, ServiceAreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows languages to be viewed or edited.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows currencies to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows service areas to be viewed or edited.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
