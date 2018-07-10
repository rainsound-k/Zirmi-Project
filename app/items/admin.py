from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Item, ItemComment


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['photo_tag', 'name', 'price']

    def photo_tag(self, item):
        if item.img:
            return mark_safe(f'<img src="{item.img.url}" style="width: 75px;"/>')
        return None


admin.site.register(ItemComment)
