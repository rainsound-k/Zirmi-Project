from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics, permissions, exceptions
from rest_framework.response import Response

from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from ..serializers import ReviewSerializer
from ..models import Review

__all__ = (
    'ReviewListCreateView',
    'ReviewRetrieveUpdateDestroyView',
    'ReviewSearchFromKeyword',
)


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = SmallPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'review_pk'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsUserOrReadOnly,
    )


class ReviewSearchFromKeyword(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        try:
            sort = self.request.query_params['sort']
            keyword = self.request.query_params['keyword']
        except MultiValueDictKeyError:
            data = {
                'detail': 'sort와 keyword를 확인해주세요'
            }
            raise exceptions.ValidationError(data)
        else:
            if keyword:
                if sort == 'title':
                    return Review.objects.filter(title__contains=keyword)
                elif sort == 'content':
                    return Review.objects.filter(content__contains=keyword)
                elif sort == 'item':
                    return Review.objects.filter(item__name__contains=keyword)
                elif sort == 'all':
                    return Review.objects.filter(
                        Q(title__contains=keyword) | Q(content__contains=keyword) | Q(
                            item__name__contains=keyword)
                    )
                else:
                    data = {
                        'detail': '올바른 sort를 입력해주세요'
                    }
                    raise exceptions.ValidationError(data)
            else:
                return Review.objects.all()

    def get(self, request, *args, **kwargs):
        if not self.get_queryset():
            data = {
                'detail': '검색결과가 없습니다'
            }
            return Response(data)
        return self.list(request, *args, **kwargs)
