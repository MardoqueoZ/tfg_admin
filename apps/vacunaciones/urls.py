from django.urls import path
from . import views

urlpatterns = [
    path('vacunaciones/<int:mascota_id>/', views.vacunaciones, name='vacunaciones'),
    path('vacunacion/crear/<int:mascota_id>/', views.crear_vacunacion, name='crear_vacunacion'),
    path('vacunacion/editar/<int:vacunacion_id>/<int:mascota_id>/', views.editar_vacunacion, name='editar_vacunacion'),
    path('vacunacion/eliminar/<int:vacunacion_id>/<int:mascota_id>/', views.eliminar_vacunacion, name='eliminar_vacunacion'),
]
