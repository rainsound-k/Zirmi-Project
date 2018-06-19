from rest_framework import generics, status
from rest_framework.response import Response

from members.serializers import UserSerializer
from ..serializers import ItemSerializer, ItemLikeSerializer
from ..models import Item

__all__ = (
    'ItemLikeToggle',
)


class ItemLikeToggle(generics.GenericAPIView):
    lookup_url_kwarg = 'item_pk'
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
        return Response(data, status=status.HTTP_201_CREATED)
