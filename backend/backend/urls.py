from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Администрация сайта'
admin.site.index_title = 'Foodgram'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]

from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_URL
    )