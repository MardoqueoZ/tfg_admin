from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('duenhos/buscar', views.buscar_duenho, name='buscar_duenho'),
    path('mascotas/<int:cedula>', views.ver_mascotas, name='ver_mascotas'),
    # apis
    path('mascotas/registrar', views.registrar_mascota),
    path('api/mascotas', views.obtener_mascotas),
    path('mascotas/<int:mascota_id>/editar', views.editar_mascota),
    path('mascotas/<int:mascota_id>/eliminar', views.eliminar_mascota),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
