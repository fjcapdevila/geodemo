from django.contrib.gis.geos import Point
from rest_framework import status, viewsets
from rest_framework.permissions import (IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Currency, Language, Provider, ServiceArea
from .permissions import IsOwner
from .serializers import (CurrencySerializer, LanguageSerializer, ProviderSerializer,
                          ServiceAreaSerializer)


class ProviderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows providers to be viewed or edited."""

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner)

    def perform_create(self, serializer):
        """Set request user as owner."""
        serializer.save(owner=self.request.user)


class LanguageViewSet(viewsets.ModelViewSet):
    """API endpoint that allows languages to be viewed or edited."""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminUser]


class CurrencyViewSet(viewsets.ModelViewSet):
    """API endpoint that allows currencies to be viewed or edited."""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAdminUser]


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """API endpoint that allows service areas to be viewed or edited."""

    queryset = ServiceArea.objects.none()
    serializer_class = ServiceAreaSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ServiceArea objects owned by request.user."""
        return ServiceArea.objects.filter(provider__owner=self.request.user)


class ProvidersByLocation(APIView):
    """
    View to list available provideers for a Location.

    Query parameters:

    - **lat**: Latitude (float) **required**.
    - **lng**: Longitude (float) **required**.

    * Only authenticated users are able to access this view.

    """

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """Return a list of providers for a Location."""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        if lat is None or lng is None:
            return Response(
                {"error": "You must provide both parameters: 'lat', 'lng'"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return Response(
                {"error": "Latitude and Longitude values must be float type"},
                status=status.HTTP_400_BAD_REQUEST)

        location = Point(lat, lng)
        queryset = ServiceArea.objects.filter(area__contains=location)
        service_areas = [ServiceAreaSerializer(instance=sa).data for sa in queryset]
        return Response(service_areas)
