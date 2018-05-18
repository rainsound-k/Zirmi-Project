from django import template

register = template.Library()


@register.filter()
def id_from_email(user):
    # rainsound128@gmail.com의 형식을 rain***** 형식으로 변경
    email = user.email
    id = email.split('@')[0]
    if len(id) < 4:
        private_id = id[:2] + '*' * 5
    else:
        private_id = id[:4] + '*' * 5
    return private_id
