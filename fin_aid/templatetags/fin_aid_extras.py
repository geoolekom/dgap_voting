from django import template
from fin_aid.models import MonthlyData, sum_by_month
register = template.Library()


@register.simple_tag
def month_info():
    text = "<h3>Сейчас: {}, Лимит: {}, Использовано: {}, Профицит: {}</h3>"
    current = MonthlyData.current()
    used = sum_by_month(current.year, current.month)
    return text.format(current.get_month_display(), current.limit, used, current.limit - used)
