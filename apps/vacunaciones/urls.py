from django.urls import path
from . import views

urlpatterns = [
    path('vacunaciones/<int:mascota_id>/', views.vacunaciones, name='vacunaciones'),
    path('vacunacione/crear/<int:mascota_id>/', views.crear_vacunacion, name='crear_vacunacion'),
    path('vacunacione/editar/<int:vacunacion_id>/<int:mascota_id>/', views.editar_vacunacion, name='editar_vacunacion'),
    path('vacunacione/eliminar/<int:vacunacion_id>/<int:mascota_id>/', views.eliminar_vacunacion, name='eliminar_vacunacion'),
    
    # APIS
    path('api/vacunaciones/<int:mascota_id>/', views.api_vacunaciones),
    path('api/vacunacione/crear/<int:mascota_id>/', views.api_crear_vacunacion),
    path('api/vacunacione/editar/<int:vacunacion_id>/<int:mascota_id>/', views.api_editar_vacunacion),
    path('api/vacunacione/eliminar/<int:vacunacion_id>/<int:mascota_id>/', views.api_eliminar_vacunacion),
]
