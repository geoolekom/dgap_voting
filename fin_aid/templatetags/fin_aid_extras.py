from django import template
from django.db.models import Sum
import os
from fin_aid.models import MonthlyData, AidRequest


register = template.Library()


@register.simple_tag
def month_info():
    text = "Сейчас: {}, Лимит: {:.0f}, Использовано: {:.0f}, Профицит: {:.0f}, Рассмаатривается: {:.0f}"
    current = MonthlyData.current()
    used = current.sum_used
    waiting = AidRequest.objects.filter(status=AidRequest.WAITING).aggregate(Sum('req_sum'))['req_sum__sum']
    if not used:
        used = 0
    return text.format(current.get_month_display(), current.limit, used, current.limit - used, waiting)
month_info.allow_tags = True


@register.filter
def filename(value):
    return os.path.basename(value.file.name)
