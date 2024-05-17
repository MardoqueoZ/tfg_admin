from django.urls import path
from . import views

urlpatterns = [
    path('vacunaciones/<int:mascota_id>/', views.vacunaciones, name='vacunaciones'),
    path('vacunaciones/crear/<int:mascota_id>/', views.crear_vacunacion, name='crear_vacunacion'),
    path('vacunaciones/editar/<int:vacunacion_id>/<int:mascota_id>/', views.editar_vacunacion, name='editar_vacunacion'),
    path('vacunaciones/eliminar/<int:vacunacion_id>/<int:mascota_id>/', views.eliminar_vacunacion, name='eliminar_vacunacion'),
    
    # APIS
    path('api/vacunaciones/<int:mascota_id>/', views.api_vacunaciones),
    path('api/vacunaciones/crear/<int:mascota_id>/', views.api_crear_vacunacion),
    path('api/vacunaciones/editar/<int:vacunacion_id>/<int:mascota_id>/', views.api_editar_vacunacion),
    path('api/vacunaciones/eliminar/<int:vacunacion_id>/<int:mascota_id>/', views.api_eliminar_vacunacion),
]
