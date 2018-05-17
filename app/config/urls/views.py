from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls.views')),
    path('', include('members.urls.views')),
    path('items/', include('items.urls.views')),
]
