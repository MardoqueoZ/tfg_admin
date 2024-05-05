from rest_framework import serializers
from .models import Mascota

# Serializador para el modelo Mascota
class MascotaSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'sexo', 'usuario', 'imagen']

