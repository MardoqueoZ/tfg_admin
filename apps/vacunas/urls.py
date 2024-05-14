from django.urls import path
from . import views


urlpatterns = [
    path('vacunas/', views.vacunas, name='vacunas'),
    path('vacunas/crear/', views.crear_vacuna, name='crear_vacuna'),
    path('vacunas/editar/<int:vacuna_id>/', views.editar_vacuna, name='editar_vacuna'),
    path('vacunas/eliminar/<int:vacuna_id>/', views.eliminar_vacuna, name='eliminar_vacuna'),
]
