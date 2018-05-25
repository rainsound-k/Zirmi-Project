from django.urls import path

from .. import views

app_name = 'reviews'

urlpatterns = [
    path('new/', views.add_review, name='add-review'),
    path('', views.review_list, name='review-list'),
]
