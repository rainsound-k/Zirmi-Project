from django.utils.datastructures import MultiValueDictKeyError
from django_filters.rest_framework import DjangoFilterBackend
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
    'ItemAddFromPublic',
)


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = SmallPagination
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = ('user__generation', 'user__gender')
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
    def get(request: object, args: object, kwargs: object) -> object:
        try:
            url = request.query_params['url']
        except MultiValueDictKeyError:
            data = {
                'detail': '검색할 url을 입력해주세요'
            }
            raise exceptions.ValidationError(data)
        else:
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
    pagination_class = SmallPagination
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


class ItemAddFromPublic(generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, *args, **kwargs):
        item_pk = self.request.data.get('pk', '')
        if not Item.objects.filter(pk=item_pk):
            raise exceptions.NotFound()
        else:
            public_item = Item.objects.get(pk=item_pk)
            if public_item.user == self.request.user:
                data = {
                    'detail': '이미 존재합니다'
                }
                return Response(data)
            else:
                Item.objects.create(
                    user=self.request.user,
                    name=public_item.name,
                    purchase_url=public_item.purchase_url,
                    price=public_item.price,
                    category=public_item.category,
                    img=public_item.img,
                    public_visibility=False,
                )
                data = {
                    'detail': '내 아이템에 추가되었습니다'
                }
                return Response(data)
