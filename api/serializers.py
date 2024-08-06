from rest_framework import serializers
from apps.consultas.models import Consulta
from apps.index.models import Usuario
from apps.mascotas.models import Mascota
from apps.tratamientos.models import Tratamiento
from apps.vacunaciones.models import Vacunacion

# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['ci', 'username','first_name', 'last_name', 'email', 'password']
        # Oculta la contraseña en la respuesta
        extra_kwargs = {
            'password': {'write_only': True}
        }

# Serializador para el modelo Consulta
class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ['fecha_consulta', 'motivo', 'indicacion', 'veterinario', 'mascota']
        
# Serializador para el modelo Mascota
class MascotaSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'sexo', 'usuario', 'imagen']

# Serializador para el modelo Tratamiento
class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'estado', 'veterinario', 'fecha_fin', 'mascota']

# Serializador para el modelo Vacunacion
class VacunacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacunacion
        fields = ['vacuna', 'dosis_aplicada', 'veterinario', 'fecha_vacunacion','mascota']