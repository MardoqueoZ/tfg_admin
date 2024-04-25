from django.urls import path
from . import views

urlpatterns = [
    path('especies/', views.especies, name='especies'),
    path('especies/crear/', views.crear_especie, name='crear_especie'),
    path('especies/editar/<int:especie_id>/', views.editar_especie, name='editar_especie'),
    path('especies/eliminar/<int:especie_id>/', views.eliminar_especie, name='eliminar_especie')
]
