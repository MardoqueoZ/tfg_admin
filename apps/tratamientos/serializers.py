from rest_framework import serializers
from .models import Tratamiento

class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'estado', 'veterinario', 'fecha_fin', 'mascota']