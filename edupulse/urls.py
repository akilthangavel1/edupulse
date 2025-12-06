from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('coursefee/', include('xcoursefee.urls')),
    path('marks/', include('xmark.urls')),
    path('faculty/', include('xtrainer.urls')),
    path('batches/', include('xbatch.urls')),
    path('transport/', include('xtransport.urls')),
    path('kits/', include('xkit.urls')),
    path('broadcast/', include('xbroadcast.urls')),
    path('system/', include('xadmin.urls')),
    path('', include('xstudent.urls')),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
