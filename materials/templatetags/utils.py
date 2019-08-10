import logging

from django import template
from django.template.defaultfilters import stringfilter
from django.utils import numberformat

logger = logging.getLogger('django.project.' + __name__)

register = template.Library()


@register.filter
def get(d, name):
    return d.get(name, '')


@register.filter
def stringify(value):
    return str(value)


@register.filter
def get_files(request, name):
    return request.FILES.getlist(name)


@register.filter
@stringfilter
def concat(first, second):
    return first + str(second)


@register.filter
def paginator_range(page_range, number):
    return page_range[number - 4 if number > 4 else 0: number + 3]


@register.filter
def money(value):
    return numberformat.format(value, decimal_sep=',', thousand_sep=' ', grouping=3, force_grouping=True)


@register.filter
@stringfilter
def startswith(first, second):
    return first.startswith(second)


@register.filter
def bool_to_text(value, variants):
    true, false = variants.split(',', 2)
    if value is True:
        return true
    elif value is False:
        return false
    else:
        return value


@register.filter
@stringfilter
def htmldiff(new_html, old_html):
    import lxml.html.diff as lxml_diff
    old_html_tokens = lxml_diff.tokenize(old_html, include_hrefs=False)
    new_html_tokens = lxml_diff.tokenize(new_html, include_hrefs=False)
    result = lxml_diff.htmldiff_tokens(old_html_tokens, new_html_tokens)
    result = ''.join(result).strip()
    return result


@register.filter
def in_kb(file):
    try:
        size = '{0:.2f} Кб'.format(file.size / 1024)
    except Exception as e:
        # logger.error(e, exc_info=True)
        return 'Файл не существует'
    else:
        return size


@register.filter
def rupluralize(value, arg=",,"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


@register.filter
def encode_except(query_dict, except_list):
    except_list = except_list.split(',')
    copy_dict = query_dict.copy()
    for e in except_list:
        if e in copy_dict:
            copy_dict.pop(e)
    return copy_dict.urlencode()
