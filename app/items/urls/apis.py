from django.urls import path

from items import apis

app_name = 'items'
urlpatterns = [
    path('', apis.ItemList.as_view(), name='items-list'),
    path('<int:pk>/', apis.ItemDetail.as_view(), name='items-detail'),
    path('<int:pk>/like/', apis.ItemLikeToggle.as_view(), name='item-like-toggle'),
]
