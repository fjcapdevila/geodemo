from django.contrib.gis.db import models

# Create your models here.


class Language(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Provider(models.Model):
    """docstring for Provider"""
    name = models.CharField(max_length=256)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    language = models.ForeignKey('Language')
    currency = models.ForeignKey('Currency')

    def __str__(self):
        return self.name
