from django.urls import path

from .. import views

app_name = 'reviews'

urlpatterns = [
    path('new/', views.new_post, name='new-post'),
    path('', views.review_list, name='review-list'),
]
