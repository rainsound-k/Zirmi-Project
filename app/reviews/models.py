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


class ReviewCommentManager(models.Manager):
    def no_reply_all(self):
        queryset = self.filter(parent=None)
        return queryset


class ReviewComment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField('')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)

    objects = ReviewCommentManager()

    class Meta:
        ordering = ['created_time']

    def children(self):
        return ReviewComment.objects.filter(parent=self)

    def __str__(self):
        return f'{self.pk}. {self.content} - {self.user}'
