from decimal import Decimal
import factory

from django.contrib.auth.models import User
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    username = factory.Sequence(lambda n: "user_%d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'secret')

class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    username = factory.Sequence(lambda n: "user_%d" % n)
    admin = True
    password = factory.PostGenerationMethodCall('set_password', 'secret')


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Currency
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: "currency_%d" % n)


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Language
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: "language_%d" % n)


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Provider
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: "provider_%d" % n)
    email = 'fake@example.com'
    phone_number = '1 800 123 4578'
    language = factory.SubFactory(LanguageFactory)
    currency = factory.SubFactory(CurrencyFactory)


class ServiceAreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ServiceArea
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: "service_area_%d" % n)
    provider = factory.SubFactory(ProviderFactory)
    price = Decimal('1.0')
