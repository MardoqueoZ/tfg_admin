from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('duenhos/buscar', views.buscar_duenho, name='buscar_duenho'),
    path('mascotas/<int:cedula>', views.ver_mascotas, name='ver_mascotas'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
