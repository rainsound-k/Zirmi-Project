import datetime

from django import template

register = template.Library()


@register.filter()
def date_formatter(date):
    # 1시간 이내로 차이날 경우는 분을, 하루 이내 차이는 시간을, 하루 이상 차이날 경우 전체 날짜를 표시
    now = datetime.datetime.now()
    if date.strftime('%Y%m%d') == now.strftime('%Y%m%d'):
        if (now - date).total_seconds() / 3600 < 1:
            min_interval = int((now - date).total_seconds() / 60)
            return f'{min_interval}분전'
        return date.strftime('%H:%M')
    else:
        return date.strftime('%Y. %-m. %d')
