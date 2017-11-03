from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django import forms
from django.db.models import Sum
from django.contrib.admin.filters import SimpleListFilter

from .models import AidRequest, Category, AidDocument, MonthlyData, Scholarship, Scholar, get_next_date, TOTAL_TAX
from .forms import SelectExportMonthForm, AidRequestAdminForm
from datetime import datetime

from notifications.notify import vk_html_user_link


class AidDocumentInline(admin.TabularInline):
    model = AidDocument


class PaymentMonthFilter(SimpleListFilter):
    title = 'Месяц выплаты'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'payment_dt'

    def lookups(self, request, model_admin):
        return (
            (1, str(MonthlyData.current())),
            (2, str(MonthlyData.next())),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        elif int(self.value()) == 1:
            current_month = MonthlyData.current()
            return queryset.filter(payment_dt=current_month.payment_dt)
        elif int(self.value()) == 2:
            next_month = MonthlyData.next()
            return queryset.filter(payment_dt=next_month.payment_dt)
        else:
            return queryset


class AidRequestAdmin(admin.ModelAdmin):
    form = AidRequestAdminForm  # (initial={"month_of_payment":AidRequestAdminForm.THIS})
    date_hierarchy = 'add_dttm'
    list_display = ['get_applicant_name', 'add_dttm', 'category', 'req_sum', 'urgent',
                    'status', 'accepted_sum', 'payment_dt', 'submitted_paper']
    list_display_links = ['get_applicant_name', 'add_dttm', 'category', 'req_sum']
    list_filter = [PaymentMonthFilter, 'status', 'category', 'urgent', 'submitted_paper', 'paid_with_cash', 'verified']
    inlines = [AidDocumentInline,]
    search_fields = ["applicant__first_name", "applicant__last_name", "reason"]
    list_editable = ["status", "accepted_sum", "payment_dt", "submitted_paper"]
    readonly_fields = ['images_tags', 'vk_link']
    fields = [('applicant', 'author'),
              ('category', 'urgent'),
              'reason',
              ('req_sum', 'accepted_sum'),
              'status',
              ('month_of_payment', 'payment_dt'),
              ('submitted_paper', 'paid_with_cash', 'verified'),
              'vk_link',
              'images_tags']

    def get_applicant_name(self, obj):
        s = "{} {}".format(obj.applicant.last_name, obj.applicant.first_name)
        if not s or s == " ":
            s = obj.applicant.username
        return s
    get_applicant_name.short_description = 'Пользователь'

    def save_model(self, request, obj, form, change):
        if obj.status in [AidRequest.ACCEPTED, AidRequest.PRE_ACCEPTED]:
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

    def get_changelist(self, request, **kwargs):
        return AidRequestChangeList

    def vk_link(self, obj):
        return vk_html_user_link(obj.applicant)
    vk_link.allow_tags = True
    vk_link.short_description = "Страница ВК"


class AidRequestChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_month = MonthlyData.current()
        used = self.queryset.filter(payment_dt=self.current_month.payment_dt).aggregate(Sum('accepted_sum'))['accepted_sum__sum']
        self.sum_used = used/TOTAL_TAX if used else 0
        waiting = self.queryset.filter(status=AidRequest.WAITING).aggregate(Sum('req_sum'))['req_sum__sum']
        self.sum_waiting = waiting/TOTAL_TAX if waiting else 0
        self.sum_max = MonthlyData.current().limit
        self.proficit = MonthlyData.current().limit - MonthlyData.current().sum_used
        self.export_form = SelectExportMonthForm()
        self.title = 'При редактировании заявлений указывайте "ЧИСТЫЕ" суммы, в статистике ниже НАЛОГ УЧТЕН'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'reason', 'max_sum', 'max_quantity', 'notifications')


class MonthlyDataAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'limit', 'deadline_dt', 'student_deadline_dt', 'payment_dt')
    list_display_links = list_display


class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'sum', 'frequency']
    list_filter = ['frequency']


class ScholarAdmin(admin.ModelAdmin):
    list_display = ['student', 'scholarship']
    list_filter = ['scholarship']


admin.site.register(Category, CategoryAdmin)
admin.site.register(AidRequest, AidRequestAdmin)
admin.site.register(AidDocument)
admin.site.register(MonthlyData, MonthlyDataAdmin)
admin.site.register(Scholarship, ScholarshipAdmin)
admin.site.register(Scholar, ScholarAdmin)
