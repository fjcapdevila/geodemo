"""
Code without tests is broken as designed.

-- Jacob Kaplan-Moss
"""

from django.contrib.gis.geos import MultiPolygon, Polygon
from django.urls import reverse
from providers.models import Currency, Language, Provider, ServiceArea
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .factories import (CurrencyFactory, LanguageFactory, ProviderFactory, ServiceAreaFactory,
                        UserFactory)


class CurrencyTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory(username='test', password='secret', is_staff=True)
        self.assertTrue(self.client.login(username='test', password='secret'))
        self.currency = CurrencyFactory(name='Test')

    def test_auth_required(self):
        client = APIClient()
        url = reverse('currency-list')
        data = {'name': 'Euro'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_currency(self):
        """Ensure we can create a new currency object."""
        url = reverse('currency-list')
        data = {'name': 'Euro'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.filter(name='Euro').count(), 1)

    def test_retrieve_currency(self):
        """Ensure we can retrieve an existing currency object."""
        url = reverse('currency-detail', args=[self.currency.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.currency.name)

    def test_update_currency(self):
        """Ensure we can update an existing currency object."""
        url = reverse('currency-detail', args=[self.currency.id])
        data = {'name': 'Real'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Currency.objects.filter(name='Real').count(), 1)

    def test_destroy_currency(self):
        """Ensure we can destroy an existing currency object."""
        url = reverse('currency-detail', args=[self.currency.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Currency.objects.count(), 0)


class LanguageTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory(username='test', password='secret', is_staff=True)
        self.assertTrue(self.client.login(username='test', password='secret'))
        self.language = LanguageFactory(name='Test')

    def test_auth_required(self):
        """Ensure authentication is required."""
        client = APIClient()
        url = reverse('language-list')
        data = {'name': 'Portuguese'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_language(self):
        """Ensure we can create a new language object."""
        url = reverse('language-list')
        data = {'name': 'Portuguese'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Language.objects.filter(name='Portuguese').count(), 1)

    def test_retrieve_language(self):
        """Ensure we can retrieve an existing language object."""
        url = reverse('language-detail', args=[self.language.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.language.name)

    def test_update_language(self):
        """Ensure we can update an existing language object."""
        url = reverse('language-detail', args=[self.language.id])
        data = {'name': 'Portuguese'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Language.objects.filter(name='Portuguese').count(), 1)

    def test_destroy_language(self):
        """Ensure we can destroy an existing language object."""
        url = reverse('language-detail', args=[self.language.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Language.objects.count(), 0)


class ProviderTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory(username='test', password='secret', is_staff=True)
        self.assertTrue(self.client.login(username='test', password='secret'))
        self.provider = ProviderFactory(name='Test', owner=self.test_user)
        self.language = LanguageFactory()
        self.currency = CurrencyFactory()

    def test_auth_required(self):
        """Ensure authentication is required."""
        client = APIClient()
        url = reverse('provider-list')
        data = {'name': 'Another Provider'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_provider(self):
        """Ensure we can create a new provider object."""
        url = reverse('provider-list')
        data = {
            'name': 'Another Provider',
            'email': 'test@example.com',
            'phone_number': '+123456789',
            'language': reverse('language-detail', args=[self.language.id]),
            'currency': reverse('currency-detail', args=[self.currency.id]),
            'service_areas': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.filter(name='Another Provider').count(), 1)

    def test_retrieve_provider(self):
        """Ensure we can retrieve an existing provider object."""
        url = reverse('provider-detail', args=[self.provider.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.provider.name)

    def test_update_provider(self):
        """Ensure we can update an existing provider object."""
        url = reverse('provider-detail', args=[self.provider.id])
        data = {
            'name': 'Black',
            'email': 'black@example.com',
            'phone_number': '+123456789',
            'language': reverse('language-detail', args=[self.language.id]),
            'currency': reverse('currency-detail', args=[self.currency.id]),
            'service_areas': []
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.filter(name='Black').count(), 1)

    def test_destroy_provider(self):
        """Ensure we can destroy an existing provider object."""
        url = reverse('provider-detail', args=[self.provider.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Provider.objects.count(), 0)


class ServiceAreaTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory(username='test', password='secret', is_staff=True)
        self.assertTrue(self.client.login(username='test', password='secret'))
        self.service_area = ServiceAreaFactory(name='Test Area')
        self.provider = self.service_area.provider
        self.provider.owner = self.test_user
        self.provider.save()

    def test_auth_required(self):
        """Ensure authentication is required."""
        client = APIClient()
        url = reverse('servicearea-list')
        data = {'name': 'Another service area'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_service_area(self):
        """Ensure we can create a new service_area object."""
        url = reverse('servicearea-list')
        data = {
            'name': 'Another service area',
            'price': 10,
            'provider': ProviderFactory(),
            'area': MultiPolygon([
                Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            ])
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceArea.objects.filter(name='Another service_area').count(), 1)

    def test_retrieve_service_area(self):
        """Ensure we can retrieve an existing service_area object."""
        url = reverse('servicearea-detail', args=[self.service_area.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.service_area.name)

    def test_update_service_area(self):
        """Ensure we can update an existing service_area object."""
        url = reverse('servicearea-detail', args=[self.service_area.id])
        data = {
            'name': 'Black service area',
            'price': 20,
            'provider': ProviderFactory(),
            'area': MultiPolygon([
                Polygon(((0, 0), (0, 2), (2, 2), (2, 0), (0, 0))),
            ])
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ServiceArea.objects.filter(name='Black').count(), 1)

    def test_destroy_service_area(self):
        """Ensure we can destroy an existing service_area object."""
        url = reverse('servicearea-detail', args=[self.service_area.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceArea.objects.count(), 0)
