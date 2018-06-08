from django.urls import path

from items import apis

app_name = 'items'
urlpatterns = [
    path('', apis.ItemListCreateView.as_view(), name='items-list'),
    path('<int:item_pk>/', apis.ItemRetrieveUpdateDestroyView.as_view(), name='items-detail'),

    # search
    path('search/', apis.ItemSearchFromURL.as_view(), name='items-search'),

    # like
    path('<int:item_pk>/like/', apis.ItemLikeToggle.as_view(), name='item-like-toggle'),

    # comment
    path('<int:item_pk>/comment/', apis.ItemCommentListCreateView.as_view(), name='item-comment-create'),
    path('comment/<int:comment_pk>/', apis.ItemCommentRetrieveUpdateDestroyView.as_view(), name='item-comment-delete'),
]
