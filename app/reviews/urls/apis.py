from django.urls import path

from reviews import apis

app_name = 'reviews'
urlpatterns = [
    path('', apis.ReviewListCreateView.as_view(), name='reviews-list'),
]
