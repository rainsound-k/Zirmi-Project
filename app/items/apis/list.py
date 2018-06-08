from rest_framework import generics, permissions
from rest_framework.response import Response

from members.serializers import UserSerializer
from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from ..serializers import ItemSerializer, ItemLikeSerializer
from ..models import Item

__all__ = (
    'ItemList',
    'ItemDetail',
    'ItemLikeToggle',
)


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = SmallPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (
        IsUserOrReadOnly,
    )


class ItemLikeToggle(generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemLikeSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        item_like, item_like_created = instance.like_user_info_list.get_or_create(user=user)
        if not item_like_created:
            item_like.delete()
            like_status = False
        else:
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'item': ItemSerializer(instance).data,
            'result': like_status,
        }
        return Response(data)
