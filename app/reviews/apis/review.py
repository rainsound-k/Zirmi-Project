from rest_framework import generics, permissions

from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from ..serializers import ReviewSerializer
from ..models import Review

__all__ = (
    'ReviewListCreateView',
    'ReviewRetrieveUpdateDestroyView',
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
