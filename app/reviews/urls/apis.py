from django.urls import path

from reviews import apis

app_name = 'reviews'
urlpatterns = [
    path('', apis.ReviewListCreateView.as_view(), name='reviews-list'),
    path('<int:review_pk>/', apis.ReviewRetrieveUpdateDestroyView.as_view(), name='reviews-detail'),

    # search
    path('search/', apis.ReviewSearchFromKeyword.as_view(), name='reviews-search'),
]
