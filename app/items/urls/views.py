from django.urls import path
from .. import views

app_name = 'items'
urlpatterns = [
    path('', views.item_list, name='index'),
    path('list/', views.my_item_list, name='my-item-list'),
]
