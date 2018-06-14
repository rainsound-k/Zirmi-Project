from django.contrib.auth import get_user_model
from rest_framework import serializers

from items.models import Item
from .models import Review, ReviewComment

__all__ = (
    'ReviewSerializer',
    'ReviewCommentSerializer',
)

User = get_user_model()


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
        )


class ReviewItemForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Item.objects.filter(user=self.context['request'].user, is_purchase=True)


class ReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)
    item = ReviewItemForeignKey(required=True)
    content = serializers.CharField(
        style={'base_template': 'textarea.html'}
    )
    view_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewCommentSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)

    class Meta:
        model = ReviewComment
        fields = (
            'pk',
            'user',
            'content',
        )
