from rest_framework import generics, permissions, exceptions
from rest_framework.response import Response

from utils.check_url_from_url_parser import CheckURL
from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from ..serializers import ItemSerializer
from ..models import Item

__all__ = (
    'ItemListCreateView',
    'ItemRetrieveUpdateDestroyView',
    'ItemSearchFromURL',
    'CompleteItemListView',
    'CompleteItemRetrieveUpdateDestroyView',
)


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = SmallPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'item_pk'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (
        IsUserOrReadOnly,
    )


class ItemSearchFromURL(generics.GenericAPIView):
    @staticmethod
    def get(request, *args, **kwargs):
        url = request.query_params['url']
        if url:
            search_result = CheckURL(url)
            search_result.check_url_from_parser()

            img_url = search_result.item_data.item_img
            price = search_result.item_data.item_price
            name = search_result.item_data.item_name
            purchase_url = search_result.item_data.url
        else:
            img_url = ''
            price = ''
            name = ''
            purchase_url = url

        data = {
            'img_url': img_url,
            'price': price,
            'name': name,
            'purchase_url': purchase_url,
        }
        return Response(data)


class CompleteItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    ordering = ('-modified_time',)
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Item.objects.filter(user=self.request.user, is_purchase=True)
        else:
            raise exceptions.NotAuthenticated()


class CompleteItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'item_pk'
    serializer_class = ItemSerializer
    permission_classes = (
        IsUserOrReadOnly,
    )

    def get_queryset(self):
        item_pk = self.kwargs.get('item_pk', None)
        user = self.request.user
        if Item.objects.filter(pk=item_pk):
            item = Item.objects.get(pk=item_pk)
            if user.is_authenticated:
                if item.user == user:
                    return Item.objects.filter(user=user, is_purchase=True, pk=item_pk)
                else:
                    raise exceptions.NotAuthenticated()
            else:
                raise exceptions.NotAuthenticated()
        else:
            raise exceptions.NotFound()
