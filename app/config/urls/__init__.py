from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import handler404

from . import apis, views
from .. import views

urlpatterns = [
    path('', include('config.urls.views')),
    path('frontend-api/', include('config.urls.apis')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

handler404 = 'config.views.page_not_found'

