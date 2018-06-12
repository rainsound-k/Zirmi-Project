from rest_framework import generics, permissions

from utils.pagination import SmallPagination
from utils.permissions import IsUserOrReadOnly
from ..serializers import ItemCommentSerializer
from ..models import Item, ItemComment

__all__ = (
    'ItemCommentListCreateView',
    'ItemCommentRetrieveUpdateDestroyView',
)


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
