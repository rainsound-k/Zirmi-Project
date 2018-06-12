from rest_framework import generics, permissions

from utils.pagination import SmallPagination
from ..serializers import ReviewSerializer
from ..models import Review

__all__ = (
    'ReviewListCreateView',
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
