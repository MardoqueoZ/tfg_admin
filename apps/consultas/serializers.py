from rest_framework import serializers
from .models import Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['fecha_consulta', 'motivo', 'indicacion', 'veterinario', 'mascota']