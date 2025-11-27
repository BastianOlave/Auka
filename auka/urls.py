from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('servicios/', include('servicios.urls')),
    path('carrito/', include('carrito.urls')),
    path('login/', include('login.urls')),
    path('catalogo/', include('catalogo.urls')),
    path('contacto/', include('contacto.urls')),
    path('novedades/', include('novedades.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
