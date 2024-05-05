from rest_framework import serializers
from .models import Mascota

# Serializador para el modelo Mascota
class MascotaSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'sexo', 'usuario', 'imagen']
        

# serializador para mostrar las mascotas de un usuario
class MascotaObtencionSerializer(serializers.ModelSerializer):
    imagenUrl = serializers.URLField(source='imagen_url', read_only=True)

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'sexo', 'usuario', 'imagenUrl']  # usar 'imagenUrl' en lugar de 'imagen_url'

