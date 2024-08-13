from django.urls import path
from . import views

urlpatterns = [
    # AUTENTICACIÓN
    path('api/login/', views.login_api),
    path('api/register/', views.register_api),
    path('api/logout/', views.logout_api),
    # ESPECIES
    path('api/especies/', views.api_especies),
    # MASCOTAS
    path('mascota/registrar/', views.registrar_mascota),
    path('api/mascotas/', views.obtener_mascotas),
    path('mascota/<int:mascota_id>/editar/', views.editar_mascota),
    path('mascota/<int:mascota_id>/eliminar/', views.eliminar_mascota),
    # NOTICIAS
    path('api/noticias/', views.api_noticias, name='api_noticias'),
    # RECOMENDACIONES
    path('api/recomendaciones/', views.api_recomendaciones),
    # TRATAMIENTOS
    path('api/tratamientos/<int:mascota_id>/', views.api_tratamientos),
    path('api/tratamiento/crear/<int:mascota_id>/', views.api_crear_tratamiento),
    path('api/tratamiento/editar/<int:tratamiento_id>/<int:mascota_id>/', views.api_editar_tratamiento),
    path('api/tratamiento/eliminar/<int:tratamiento_id>/<int:mascota_id>/', views.api_eliminar_tratamiento),
    # VACUNACIONES
    path('api/vacunaciones/<int:mascota_id>/', views.api_vacunaciones),
    path('api/vacunacion/crear/<int:mascota_id>/', views.api_crear_vacunacion),
    path('api/vacunacion/editar/<int:vacunacion_id>/<int:mascota_id>/', views.api_editar_vacunacion),
    path('api/vacunacion/eliminar/<int:vacunacion_id>/<int:mascota_id>/', views.api_eliminar_vacunacion),
    # CONSULTAS
    path('api/consultas/<int:mascota_id>/', views.api_consultas),
    path('api/consulta/crear/<int:mascota_id>/', views.api_crear_consulta),
    path('api/consulta/editar/<int:consulta_id>/<int:mascota_id>/', views.api_editar_consulta),
    path('api/consulta/eliminar/<int:consulta_id>/<int:mascota_id>/', views.api_eliminar_consulta),
]
