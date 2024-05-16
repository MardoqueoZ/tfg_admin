from django.urls import path
from . import views

urlpatterns = [
    path('consultas/<int:mascota_id>/', views.consultas, name='consultas'),
    path('consultas/crear/<int:mascota_id>/', views.crear_consulta, name='crear_consulta'),
    path('consultas/editar/<int:consulta_id>/<int:mascota_id>/', views.editar_consulta, name='editar_consulta'),
    path('consultas/ver/<int:consulta_id>/<int:mascota_id>/', views.ver_consulta, name='ver_consulta'),
    path('consultas/eliminar/<int:consulta_id>/<int:mascota_id>/', views.eliminar_consulta, name='eliminar_consulta'),
]