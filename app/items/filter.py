import django_filters

from items.models import Item

__all__ = (
    'ItemFilter',
)


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = (
            'user__generation',
            'user__gender',
            'category',
        )
