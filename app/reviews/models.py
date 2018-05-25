from django.contrib.auth import get_user_model
from django.db import models

from django_summernote import models as summer_model
from django_summernote import fields as summer_fields

from core.models import TimeStampedModel
from items.models import Item

User = get_user_model()


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class Review(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_reviews',
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.CharField('제목', max_length=200)
    content = models.TextField('내용', default='')
    view_count = models.IntegerField('조회수', default=0)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.title} - {self.user}'
