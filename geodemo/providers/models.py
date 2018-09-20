from django.contrib.gis.db import models

# Create your models here.


class Language(models.Model):
    name = models.CharField(max_length=256, blank=False, unique=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=256, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name


def get_default_language():
    return Language.objects.get_or_create(name='English')[0]


def get_default_currency():
    return Currency.objects.get_or_create(name='US Dollar')[0]


class Provider(models.Model):
    """docstring for Provider"""
    name = models.CharField(max_length=256, blank=False, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    language = models.ForeignKey('Language', on_delete=models.SET(get_default_language))
    currency = models.ForeignKey('Currency', on_delete=models.SET(get_default_currency))

    def __str__(self):
        return self.name
