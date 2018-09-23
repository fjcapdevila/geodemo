from django.test import TestCase
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .factories import (CurrencyFactory, LanguageFactory, ProviderFactory, ServiceAreaFactory,
                        UserFactory)
from providers.serializers import (CurrencySerializer, LanguageSerializer,
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
            'currency': CurrencyFactory(name="Argentine Peso"),
            'owner': UserFactory()
        }

        self.provider = ProviderFactory(**self.provider_attributes)
        self.serializer = ProviderSerializer(instance=self.provider, context=serializer_context)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['name', 'email', 'phone_number', 'language', 'currency', 'service_areas', 'owner'])

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

    def test_owner_field_content(self):
        data = self.serializer.data
        owner = self.provider_attributes['owner']
        self.assertEqual(data['owner'], owner.username)


class TestServiceAreaSerializer(TestCase):

    def setUp(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        serializer_context = {'request': Request(request)}
        self.service_area = ServiceAreaFactory()
        self.provider = ProviderFactory(name="Local Provider")
        self.service_area_attributes = {
            'name': 'base area',
            'provider': self.provider,
            'area': self.service_area
        }
        self.serializer = ServiceAreaSerializer(instance=self.service_area,
                                                context=serializer_context)

    # def test_contains_expected_fields(self):
    #     data = self.serializer.data
    #     self.assertCountEqual(data.keys(), ['name', 'provider', 'area'])

    # def test_name_field_content(self):
    #     data = self.serializer.data
    #     self.assertEqual(data['name'], self.language_attributes['name'])

    # def test_provider_field_content(self):
    #     data = self.serializer.data
    #     self.assertEqual(data['email'], self.language_attributes['email'])

    # def test_area_field_content(self):
    #     data = self.serializer.data
    #     self.assertEqual(data['phone_number'], self.language_attributes['phone_number'])
