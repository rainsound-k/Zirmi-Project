from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('config.urls.views')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)