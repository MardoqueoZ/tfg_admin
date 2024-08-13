from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('editar/rol/<int:usuario_id>/', views.editar_rol, name='editar_rol'),
    path('auditoria/usuarios', views.auditoria_usuarios, name='auditoria_usuarios'),
]
