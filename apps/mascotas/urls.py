from django.urls import path
from . import views

urlpatterns = [
    path('duenhos/buscar', views.buscar_duenho, name='buscar_duenho'),
    path('mascotas/<int:cedula>', views.ver_mascotas, name='ver_mascotas')
]
