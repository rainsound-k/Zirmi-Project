from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Review, ReviewComment


class ReviewModelAdmin(SummernoteModelAdmin):
    pass


admin.site.register(Review, ReviewModelAdmin)
admin.site.register(ReviewComment)
