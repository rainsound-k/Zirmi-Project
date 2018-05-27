import datetime

from django import template

register = template.Library()


@register.filter()
def date_formatter(date):
    now = datetime.datetime.now()
    if date.strftime('%Y%m%d') == now.strftime('%Y%m%d'):
        if (now - date).total_seconds() / 3600 < 1:
            min_interval = int((now - date).total_seconds() / 60)
            return f'{min_interval}분전'
        return date.strftime('%H:%M')
    else:
        return date.strftime('%Y. %-m. %d')
