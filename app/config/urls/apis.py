from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('items/', include('items.urls.apis')),
    path('members/', include('members.urls.apis')),
    path('reviews/', include('reviews.urls.apis')),
]
