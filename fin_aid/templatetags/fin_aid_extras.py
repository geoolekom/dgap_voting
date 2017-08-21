from django import template
from fin_aid.models import MonthlyData
register = template.Library()


@register.simple_tag
def month_info():
    text = "<h3>Сейчас: {}, Лимит: {}, Использовано: {}, Профицит: {}</h3>"
    current = MonthlyData.current()
    used = current.sum_used
    if not used:
        used = 0
    return text.format(current.get_month_display(), current.limit, used, current.limit - used)
