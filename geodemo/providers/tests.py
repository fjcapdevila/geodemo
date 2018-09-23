"""
Code without tests is broken as designed.

-- Jacob Kaplan-Moss
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from .factories import (AdminFactory, CurrencyFactory, LanguageFactory,
                        ProviderFactory, ServiceAreaFactory, UserFactory)
from .models import Currency, Language, Provider, ServiceArea
from .serializers import (CurrencySerializer, LanguageSerializer,
                          ProviderSerializer, ServiceAreaSerializer)


class TestCurrencySerializer(TestCase):
    def setUp(self):
        """Create some useful objects for testing."""
        self.currency_attributes = {"name": "Euro"}
        self.currency = CurrencyFactory(**self.currency_attributes)
        self.serializer = CurrencySerializer(instance=self.currency)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['name'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.currency_attributes['name'])


class TestLanguageSerializer(TestCase):
    def setUp(self):
        self.language_attributes = {"name": "Swedish"}
        self.language = LanguageFactory(**self.language_attributes)
        self.serializer = LanguageSerializer(instance=self.language)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['name'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.language_attributes['name'])


class TestProviderSerializer(TestCase):
    def setUp(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        serializer_context = {'request': Request(request)}

        self.provider_attributes = {
            'name': 'fast',
            'email': 'contact@fast.com',
            'phone_number': '+18002345678',
            'language': LanguageFactory(name="Spanish"),
            'currency': CurrencyFactory(name="Argentine Peso")
        }

        self.provider = ProviderFactory(**self.provider_attributes)
        self.serializer = ProviderSerializer(instance=self.provider, context=serializer_context)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['name', 'email', 'phone_number', 'language', 'currency', 'service_areas'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.provider_attributes['name'])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.provider_attributes['email'])

    def test_phone_number_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['phone_number'], self.provider_attributes['phone_number'])

    def test_language_field_content(self):
        data = self.serializer.data
        language = self.provider_attributes['language']
        self.assertIn(reverse('language-detail', args=[language.id]), data['language'])

    def test_currency_field_content(self):
        data = self.serializer.data
        currency = self.provider_attributes['currency']
        self.assertIn(reverse('currency-detail', args=[currency.id]), data['currency'])


# class TestServiceAreaSerializer(TestCase):

#     def setUp(self):
#         factory = APIRequestFactory()
#         request = factory.get('/')
#         serializer_context = {'request': Request(request)}
#         self.service_area = ServiceArea.objects.create(name="Local area")
#         self.provider =
#         self.service_area_attributes = {
#                 'name': 'base area',
#                 'provider':
#                 'area': None
#         }

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertCountEqual(data.keys(), ['name', 'provider', 'area'])

#     def test_name_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['name'], self.language_attributes['name'])

#     def test_provider_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['email'], self.language_attributes['email'])

#     def test_area_field_content(self):
#         data = self.serializer.data
#         self.assertEqual(data['phone_number'], self.language_attributes['phone_number'])


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
        """
        Ensure we can create a new currency object.
        """
        url = reverse('currency-list')
        data = {'name': 'Euro'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.filter(name='Euro').count(), 1)

    def test_retrieve_currency(self):
        """
        Ensure we can retrieve an existing currency object.
        """
        url = reverse('currency-detail', args=[self.currency.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.currency.name)

    def test_update_currency(self):
        """
        Ensure we can update an existing currency object.
        """
        url = reverse('currency-detail', args=[self.currency.id])
        data = {'name': 'Real'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Currency.objects.filter(name='Real').count(), 1)

    def test_destroy_currency(self):
        """
        Ensure we can destroy an existing currency object.
        """
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
        client = APIClient()
        url = reverse('language-list')
        data = {'name': 'Portuguese'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_language(self):
        """
        Ensure we can create a new language object.
        """
        url = reverse('language-list')
        data = {'name': 'Portuguese'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Language.objects.filter(name='Portuguese').count(), 1)

    def test_retrieve_language(self):
        """
        Ensure we can retrieve an existing language object.
        """
        url = reverse('language-detail', args=[self.language.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.language.name)

    def test_update_language(self):
        """
        Ensure we can update an existing language object.
        """
        url = reverse('language-detail', args=[self.language.id])
        data = {'name': 'Real'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Language.objects.filter(name='Real').count(), 1)

    def test_destroy_language(self):
        """
        Ensure we can destroy an existing language object.
        """
        url = reverse('language-detail', args=[self.language.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Language.objects.count(), 0)
