from django import template
import os
from fin_aid.models import MonthlyData


register = template.Library()


@register.simple_tag
def month_info():
    text = "Сейчас: {}, Лимит: {}, Использовано: {}, Профицит: {}"
    current = MonthlyData.current()
    used = current.sum_used
    if not used:
        used = 0
    return text.format(current.get_month_display(), current.limit, used, current.limit - used)
month_info.allow_tags = True


@register.filter
def filename(value):
    return os.path.basename(value.file.name)
