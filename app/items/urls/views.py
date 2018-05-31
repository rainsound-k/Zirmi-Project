from django.urls import path
from .. import views

app_name = 'items'
urlpatterns = [
    path('list/', views.my_item_list, name='my-item-list'),
    path('list/complete/', views.my_complete_item_list, name='my-complete-item-list'),
    path('search/', views.search_url, name='search-url'),
    path('search/add/', views.item_add, name='item-add'),

    path('<int:item_pk>/', views.item_detail, name='item-detail'),
    path('<int:item_pk>/edit/', views.item_edit, name='item-edit'),
    path('delete/', views.item_delete, name='item-delete'),
    path('complete/', views.purchase_complete, name='purchase-complete'),
    path('complete/<int:item_pk>/', views.purchase_item_detail, name='purchase-item-detail'),

    path('public/<int:item_pk>/', views.public_item_detail, name='public-item-detail'),
    path('public/add/', views.add_from_public, name='add-from-public'),
    path('public/like/', views.item_like_toggle, name='item-like-toggle'),

    # comment
    path('public/<int:item_pk>/comment/create/', views.comment_create, name='comment-create'),
    path('public/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment-delete'),

]
