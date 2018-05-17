from django.urls import path
from .. import views

app_name = 'items'
urlpatterns = [
    path('list/', views.my_item_list, name='my-item-list'),
    path('add/', views.item_add, name='item-add'),
    path('<int:item_pk>/', views.item_detail, name='item-detail'),
    path('public/<int:item_pk>/', views.public_item_detail, name='public-item-detail'),
    path('<int:item_pk>/edit/', views.item_edit, name='item-edit'),
]
