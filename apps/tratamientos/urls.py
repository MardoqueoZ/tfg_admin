from django.urls import path
from . import views

urlpatterns = [
    path('tratamientos/<int:mascota_id>/', views.tratamientos, name='tratamientos'),
    path('crear_tratamiento/<int:mascota_id>/', views.crear_tratamiento, name='crear_tratamiento'),
    path('editar_tratamiento/<int:tratamiento_id>/<int:mascota_id>/', views.editar_tratamiento, name='editar_tratamiento'),
    path('ver_tratamiento/<int:tratamiento_id>/<int:mascota_id>/', views.ver_tratamiento, name='ver_tratamiento'),
    path('eliminar_tratamiento/<int:tratamiento_id>/<int:mascota_id>/', views.eliminar_tratamiento, name='eliminar_tratamiento'),
    
    # APIS
    path('api/tratamientos/<int:mascota_id>/', views.api_tratamientos),
    path('api/tratamiento/crear/<int:mascota_id>/', views.api_crear_tratamiento),
    path('api/tratamiento/editar/<int:tratamiento_id>/<int:mascota_id>/', views.api_editar_tratamiento),
    path('api/tratamiento/eliminar/<int:tratamiento_id>/<int:mascota_id>/', views.api_eliminar_tratamiento),
]
