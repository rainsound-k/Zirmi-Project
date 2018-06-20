from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Item, ItemLike, ItemComment

__all__ = (
    'ItemSerializer',
    'ItemLikeSerializer',
    'ItemCommentSerializer',
)
User = get_user_model()


class ItemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
        )


class ItemSerializer(serializers.ModelSerializer):
    user = ItemUserSerializer(many=False, read_only=True)
    public_visibility = serializers.BooleanField(default=True)
    like_users = ItemUserSerializer(many=True, read_only=True)
    category = serializers.ChoiceField(choices=Item.CHOICES_CATEGORY, source='get_category_display')
    is_purchase = serializers.BooleanField(default=False)
    purchase_date = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = Item
        fields = '__all__'


class ItemLikeSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    user = ItemUserSerializer(read_only=True, many=True)

    class Meta:
        model = ItemLike
        fields = '__all__'


class ItemCommentSerializer(serializers.ModelSerializer):
    user = ItemUserSerializer(read_only=True)

    class Meta:
        model = ItemComment
        fields = (
            'pk',
            'user',
            'content',
        )
