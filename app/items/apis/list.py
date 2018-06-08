from rest_framework import generics, permissions
from rest_framework.response import Response

from members.serializers import UserSerializer
from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from utils.url_parser import ItemData
from ..serializers import ItemSerializer, ItemLikeSerializer, ItemCommentSerializer
from ..models import Item, ItemComment

__all__ = (
    'ItemListCreateView',
    'ItemRetrieveUpdateDestroyView',
    'ItemLikeToggle',
    'ItemCommentListCreateView',
    'ItemCommentRetrieveUpdateDestroyView',
    'ItemSearchFromURL',
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
        return Response(data)


class ItemCommentListCreateView(generics.ListCreateAPIView):
    lookup_url_kwarg = 'item_pk'
    serializer_class = ItemCommentSerializer
    pagination_class = SmallPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        item_pk = self.kwargs.get(self.lookup_url_kwarg)
        comments = ItemComment.objects.filter(item__pk=item_pk)
        return comments

    def perform_create(self, serializer):
        item_pk = self.kwargs.get(self.lookup_url_kwarg)
        item = Item.objects.get(pk=item_pk)
        serializer.save(user=self.request.user, item=item)


class ItemCommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'comment_pk'
    queryset = ItemComment.objects.all()
    serializer_class = ItemCommentSerializer
    permission_classes = (
        IsUserOrReadOnly,
    )


class ItemSearchFromURL(generics.GenericAPIView):
    @staticmethod
    def get(request, *args, **kwargs):
        url = request.query_params['url']
        if url:
            item_data = ItemData(request, url)
            if '11st.co.kr' in url:
                item_data.get_info_from_11st()

            elif 'gmarket.co.kr' in url:
                item_data.get_info_from_gmarket()

            elif 'auction.co.kr' in url:
                item_data.get_info_from_auction()

            elif 'interpark.com' in url:
                item_data.get_info_from_interpark()

            elif 'smartstore.naver.com' in url:
                item_data.get_info_from_naver_store()

            elif 'naver.me' in url:
                item_data.get_info_from_naver_short_url()

            elif 'lotteimall.com' in url:
                item_data.get_info_from_lotte_mall()

            elif 'lotte.com' in url:
                item_data.get_info_from_lotte_dot_com()

            elif 'hyundaihmall.com' in url:
                item_data.get_info_from_hyundai()

            elif 'ssg.com' in url:
                item_data.get_info_from_ssg()

            elif 'gsshop.com' in url:
                item_data.get_info_from_gs()

            elif 'galleria.co.kr' in url:
                item_data.get_info_from_galleria()

            elif 'akmall.com' in url:
                item_data.get_info_from_ak()

            elif 'nsmall.com' in url:
                item_data.get_info_from_ns()

            elif 'coupang.com' in url:
                item_data.get_info_from_coupang()

            elif 'wemakeprice.com' in url:
                item_data.get_info_from_wemakeprice()

            elif 'ticketmonster.co.kr' in url:
                item_data.get_info_from_tmon()

            elif 'g9.co.kr' in url or 'g9ro.kr' in url:
                item_data.get_info_from_g9()

            item_img = item_data.item_img
            item_price = item_data.item_price
            item_name = item_data.item_name
            url = item_data.url
        else:
            item_img = ''
            item_price = ''
            item_name = ''
            url = url

        data = {
            'item_img': item_img,
            'item_price': item_price,
            'item_name': item_name,
            'url': url,
        }
        return Response(data)
