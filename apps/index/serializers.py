from rest_framework import serializers
from .models import Usuario

# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['ci', 'username','first_name', 'last_name', 'email', 'password']
        # Oculta la contraseña en la respuesta
        extra_kwargs = {
            'password': {'write_only': True}
        }
        

# class UsuarioLoginSerializer(serializers.Serializer):
#     ci = serializers.IntegerField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(username=data['ci'], password=data['password'])
#         if user:
#             return user
#         raise serializers.ValidationError('Credenciales inválidas')
