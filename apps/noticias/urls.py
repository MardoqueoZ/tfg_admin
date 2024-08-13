from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/crear/', views.crear_noticia, name='crear_noticia'),
    path('noticias/editar/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/ver/<int:noticia_id>/', views.ver_noticia, name='ver_noticia'),
    path('noticias/eliminar/<int:noticia_id>/', views.eliminar_noticia, name='eliminar_noticia'),
    path('auditoria/noticias/', views.auditoria_noticias, name='auditoria_noticias'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
