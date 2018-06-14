from rest_framework import generics, permissions

from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from ..serializers import ReviewCommentSerializer
from ..models import Review, ReviewComment

__all__ = (
    'ReviewCommentListCreateView',
    'ReviewCommentRetrieveUpdateDestroyView',
)


class ReviewCommentListCreateView(generics.ListCreateAPIView):
    lookup_url_kwarg = 'review_pk'
    serializer_class = ReviewCommentSerializer
    pagination_class = SmallPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review_pk = self.kwargs.get(self.lookup_url_kwarg)
        comments = ReviewComment.objects.filter(review__pk=review_pk)
        return comments

    def perform_create(self, serializer):
        review_pk = self.kwargs.get(self.lookup_url_kwarg)
        review = Review.objects.get(pk=review_pk)
        serializer.save(user=self.request.user, review=review)


class ReviewCommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'comment_pk'
    queryset = ReviewComment.objects.all()
    serializer_class = ReviewCommentSerializer
    permission_classes = (
        IsUserOrReadOnly,
    )
