from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('api/login', views.login_api),
    path('api/register', views.register_api),
    path('api/logout', views.logout_api),
]
