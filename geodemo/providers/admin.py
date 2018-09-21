
from django.contrib.gis import admin
from .models import Currency, Language, Provider, ServiceArea


admin.site.register(Currency)
admin.site.register(Language)
admin.site.register(Provider)
admin.site.register(ServiceArea, admin.OSMGeoAdmin)
