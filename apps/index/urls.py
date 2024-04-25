from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    re_path('api/login', views.login_api),
    re_path('api/register', views.register_api),
    re_path('api/logout', views.logout_api),
]
