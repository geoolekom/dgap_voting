from django.contrib import admin
from cycle_storage.models import Bicycle, Storage, Place


class BicycleAdmin(admin.ModelAdmin):
    list_display = ("owner", "manufacturer", "model", "place", "verified", "request_status")


class StorageAdmin(admin.ModelAdmin):
    list_display = ("dorm", "name", "total_places", "free_places")


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("__str__", "bicycle")

admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Place, PlaceAdmin)
