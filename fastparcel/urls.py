from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shipping.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shipping.urls'), name='fastparcel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
