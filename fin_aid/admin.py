from django.contrib import admin
from django import forms
from .models import AidRequest, Category, AidDocument, MonthlyData, get_next_date
from datetime import datetime


class AidDocumentInline(admin.TabularInline):
    model = AidDocument


class AidRequestAdminForm(forms.ModelForm):
    THIS = 1
    NEXT = 2
    FOLLOWING = 3
    MONTHS = [(THIS, "Ближайший месяц"),
              (NEXT, "Следующий месяц"),
              (FOLLOWING, "Через месяц"),]
    month_of_payment = forms.ChoiceField(choices=MONTHS, label="Месяц выплаты")

    class Meta:
        model = AidRequest
        exclude = ["payment_dt", "examination_dttm"]


class AidRequestAdmin(admin.ModelAdmin):
    form = AidRequestAdminForm  # (initial={"month_of_payment":AidRequestAdminForm.THIS})
    date_hierarchy = 'add_dttm'
    list_display = ['get_applicant_name', 'add_dttm', 'category', 'req_sum', 'urgent',
                    'status', 'accepted_sum', 'payment_dt', 'submitted_paper']
    list_display_links = ['get_applicant_name', 'add_dttm', 'category', 'req_sum']
    list_filter = ('status', 'category', 'urgent', 'add_dttm', 'submitted_paper')
    inlines = [AidDocumentInline,]
    search_fields = ["applicant__first_name", "applicant__last_name", "reason"]
    list_editable = ["status", "accepted_sum", "payment_dt", "submitted_paper"]
    readonly_fields = ['images_tags']

    def get_applicant_name(self, obj):
        s = "{} {}".format(obj.applicant.last_name, obj.applicant.first_name)
        if not s or s == " ":
            s = obj.applicant.username
        return s
    get_applicant_name.short_description = 'Пользователь'

    def save_model(self, request, obj, form, change):
        if obj.status == AidRequest.ACCEPTED:
            if not obj.accepted_sum:
                obj.accepted_sum = obj.req_sum
            if not obj.payment_dt:
                month = form.cleaned_data['month_of_payment'] if "month_of_payment" in form.cleaned_data else None
                if not month or month == str(AidRequestAdminForm.THIS):
                    obj.payment_dt = get_next_date(None, 'payment')
                elif month == str(AidRequestAdminForm.NEXT):
                    obj.payment_dt = get_next_date(get_next_date(None, 'payment'), 'payment')
                elif month == str(AidRequestAdminForm.FOLLOWING):
                    obj.payment_dt = get_next_date(get_next_date(get_next_date(None, 'payment'), 'payment'), 'payment')
        if obj.status != AidRequest.WAITING:
            obj.examination_dttm = datetime.now()
        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'reason', 'max_sum', 'max_quantity', 'notifications')


class MonthlyDataAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'limit', 'deadline_dt', 'payment_dt')
    list_display_links = list_display

admin.site.register(Category, CategoryAdmin)
admin.site.register(AidRequest, AidRequestAdmin)
admin.site.register(AidDocument)
admin.site.register(MonthlyData, MonthlyDataAdmin)
