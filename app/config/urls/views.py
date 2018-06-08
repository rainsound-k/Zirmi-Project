from django.contrib import admin
from django.urls import path, include

from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.item_list, name='index'),
    path('', include('members.urls.views')),
    path('items/', include('items.urls.views')),
    path('reviews/', include('reviews.urls.views')),
    path('summernote/', include('django_summernote.urls')),
]
