from django.contrib import admin
from django import forms
from .models import AidRequest, Category, AidDocument, get_next_payment_dttm
from django.contrib.admin.filters import DateFieldListFilter

from notifications.notify import notify
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
        exclude = ["payment_dttm", "examination_dttm"]


class AidRequestAdmin(admin.ModelAdmin):
    form = AidRequestAdminForm#(initial={"month_of_payment":AidRequestAdminForm.THIS})
    date_hierarchy = 'add_dttm'
    prepopulated_fields = {"accepted_sum": ("req_sum",)}
    list_display = ('applicant', 'add_dttm', 'category', 'req_sum', 'urgent', 'status', 'accepted_sum', 'payment_dttm', 'submitted_paper')
    #list_display_links = list_display
    list_filter = ('status', 'category', 'urgent', 'add_dttm', 'submitted_paper')
    inlines = [AidDocumentInline,]
    search_fields = ["applicant__first_name", "applicant__last_name", "reason"]
    list_editable = ["status", "accepted_sum", "payment_dttm", "submitted_paper"]

    def save_model(self, request, obj, form, change):
        if obj.status == AidRequest.ACCEPTED:
            if not obj.accepted_sum:
                obj.accepted_sum = obj.req_sum
            if not obj.payment_dttm:
                month = form.cleaned_data['month_of_payment']
                print(get_next_payment_dttm())
                print(month)
                print(AidRequestAdminForm.THIS)
                if not month or month == str(AidRequestAdminForm.THIS):
                    obj.payment_dttm = get_next_payment_dttm()
                    print("KEK")
                elif month == str(AidRequestAdminForm.NEXT):
                    obj.payment_dttm = get_next_payment_dttm(get_next_payment_dttm())
                elif month == str(AidRequestAdminForm.FOLLOWING):
                    obj.payment_dttm = get_next_payment_dttm(get_next_payment_dttm(get_next_payment_dttm()))
        if obj.status != AidRequest.WAITING:
            obj.examination_dttm = datetime.now()
            s = "Статус заявления на матпомощь от {} по категории {} изменен на '{}'\n".format(obj.add_dttm.date(),
                                                                                               obj.category,
                                                                                               obj.status)
            if obj.status == obj.ACCEPTED:
                s += "Одобренная сумма: {}\nОжидаемая дата выплаты: {}\n".format(obj.accepted_sum, obj.payment_dttm)
            if obj.examination_comment:
                s += "Комментарий стип. комиссии: {}\n".format(obj.examination_comment)
            notify(obj.applicant, s)

        obj.save()


class Categoryadmin(admin.ModelAdmin):
    list_display = ('name', 'reason', 'max_sum', 'max_quantity')


admin.site.register(Category, Categoryadmin)
admin.site.register(AidRequest, AidRequestAdmin)
admin.site.register(AidDocument)
