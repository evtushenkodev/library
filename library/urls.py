from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from library import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('books.urls')),
]
urlpatterns += swagger.urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
