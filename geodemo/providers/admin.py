from django.contrib.gis import admin

from .models import Currency, Language, Provider, ServiceArea


class ProviderAdmin(admin.ModelAdmin):
    """Custom Admin for Providers."""
    list_display = ('name', 'owner')


admin.site.register(Currency)
admin.site.register(Language)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(ServiceArea, admin.OSMGeoAdmin)
