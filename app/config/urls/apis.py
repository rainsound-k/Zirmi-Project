from django.urls import path, include

app_name = 'apis'
urlpatterns = [
    path('items/', include('items.urls.apis')),
    path('members/', include('members.urls.apis')),
]