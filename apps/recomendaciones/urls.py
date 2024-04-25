from django.urls import path
from . import views

urlpatterns = [
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    path('recomendaciones/crear/', views.crear_recomendacion, name='crear_reco'),
    path('recomendaciones/editar/<int:reco_id>', views.editar_recomendacion, name='editar_reco'),
    path('recomendaciones/ver/<int:reco_id>', views.ver_recomendacion, name='ver_reco'),
    path('recomendaciones/eliminar/<int:reco_id>', views.eliminar_recomendacion, name='eliminar_reco'),
]
