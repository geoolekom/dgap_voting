from django.contrib import admin
from .models import AidRequest, Category, AidDocument, get_next_payment_dttm
from django.contrib.admin.filters import DateFieldListFilter

from datetime import datetime


class AidDocumentInline(admin.TabularInline):
    model = AidDocument


class AidRequestAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'add_dttm', 'category', 'req_sum', 'urgent', 'status', 'accepted_sum', 'payment_dttm', 'submitted_paper')
    #list_display_links = list_display
    list_filter = ('status', 'category', 'urgent', 'add_dttm', 'submitted_paper')
    inlines = [AidDocumentInline,]
    # radio_fields = {"category": admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        if obj.status == AidRequest.ACCEPTED:
            if not obj.accepted_sum:
                obj.accepted_sum = obj.req_sum
            if not obj.payment_dttm:
                obj.payment_dttm = get_next_payment_dttm()
        if obj.status != AidRequest.WAITING:
            obj.examination_dttm = datetime.now()
        obj.save()


class Categoryadmin(admin.ModelAdmin):
    list_display = ('name', 'reason', 'max_sum', 'max_quantity')


admin.site.register(Category, Categoryadmin)
admin.site.register(AidRequest, AidRequestAdmin)
admin.site.register(AidDocument)
