from django import template
from django.contrib.auth.decorators import login_required

from ..models import Item

register = template.Library()


@login_required
@register.simple_tag
def check_item_exists(item, request):
    public_item_name = item.name
    public_item_price = item.price
    user_items = Item.objects.filter(user=request.user)

    for user_item in user_items:
        if user_item.name == public_item_name and user_item.price == public_item_price:
            return True
    return False
