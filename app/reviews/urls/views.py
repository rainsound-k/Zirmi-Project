from django.urls import path

from .. import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review-list'),
    path('add/', views.add_review, name='add-review'),
    path('<int:review_pk>/', views.view_review, name='view-review'),
]
