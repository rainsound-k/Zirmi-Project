from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Item, ItemLike

__all__ = (
    'ItemSerializer',
    'ItemLikeSerializer',
)


class ItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class ItemLikeSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ItemLike
        fields = '__all__'
