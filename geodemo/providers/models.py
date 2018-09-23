from django.contrib.gis.db import models

from django.core.validators import MinValueValidator, DecimalValidator


class Language(models.Model):
    """Language."""

    name = models.CharField(max_length=256, blank=False, unique=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Currency."""

    name = models.CharField(max_length=256, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name


def get_default_language():
    """Create the default language."""
    return Language.objects.get_or_create(name='English')[0]


def get_default_currency():
    """Create the default currency."""
    return Currency.objects.get_or_create(name='US Dollar')[0]


class Provider(models.Model):
    """Represents a provider."""

    owner = models.ForeignKey(
        'auth.User', null=True, related_name='providers', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    language = models.ForeignKey('Language', on_delete=models.SET(get_default_language))
    currency = models.ForeignKey('Currency', on_delete=models.SET(get_default_currency))

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """Represents a service area covered by a provider."""

    name = models.CharField(max_length=50, unique=True)
    provider = models.ForeignKey(
        'Provider', null=False, related_name='service_areas', on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
        validators=[MinValueValidator(0), DecimalValidator(10, 4)])
    area = models.MultiPolygonField()

    def __str__(self):
        return self.name
