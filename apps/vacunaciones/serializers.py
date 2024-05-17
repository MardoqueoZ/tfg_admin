from rest_framework import serializers
from .models import Vacunacion

# Serializador para el modelo Vacunacion
class VacunacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacunacion
        fields = ['vacuna', 'dosis_aplicada', 'veterinario', 'fecha_vacunacion','mascota']