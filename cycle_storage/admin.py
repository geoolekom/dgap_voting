from django.contrib import admin
from cycle_storage.models import Bicycle, Storage, Place


class BicycleAdmin(admin.ModelAdmin):
    list_display = ("owner", "manufacturer", "model", "place", "verified")


class StorageAdmin(admin.ModelAdmin):
    list_display = ("dorm", "name", "total_places", "free_places")


admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Place)
