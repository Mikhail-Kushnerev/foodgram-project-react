from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Администрация сайта'
admin.site.index_title = 'Foodgram'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_URL
    )
