from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from cycle_storage.models import Bicycle, Storage, Place

from .forms import BicycleAdminForm


class PlaceFilter(SimpleListFilter):
    title = 'Присвоено место'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'place'

    def lookups(self, request, model_admin):
        return (
            (1, 'Есть место'),
            (0, 'Нет места'),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        elif int(self.value()) == 1:
            return queryset.exclude(place=None)
        else:
            return queryset.filter(place=None)


class BicycleAdmin(admin.ModelAdmin):
    list_display = ("owner", "manufacturer", "model", "place", "verified", "request_status")
    list_filter = ("verified", "request_status", PlaceFilter)
    readonly_fields = ["image_tag"]
    form = BicycleAdminForm

    def save_model(self, request, obj, form, change):
        if "place" in form.cleaned_data:
            place = form.cleaned_data["place"]
            place.bicycle = obj
            place.save()
        super(BicycleAdmin, self).save_model(request, obj, form, change)


class StorageAdmin(admin.ModelAdmin):
    list_display = ("dorm", "name", "total_places", "free_places")


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("__str__", "bicycle")


admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Place, PlaceAdmin)
