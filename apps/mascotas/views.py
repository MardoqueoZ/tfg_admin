from django.shortcuts import render
from .models import Mascota
from django.contrib.auth.decorators import login_required
from apps.index.models import Usuario
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import MascotaSerializer
import pyrebase
import uuid


# configuracion firebase storage
config = {
    "apiKey": "AIzaSyAKM1RT0QNYwYQfQ_bhoZk72urS6OK4PJE",
    "authDomain": "tfgapp-385f5.firebaseapp.com",
    "projectId": "tfgapp-385f5",
    "storageBucket": "tfgapp-385f5.appspot.com",
    "messagingSenderId": "53852604577",
    "appId": "1:53852604577:web:d4b78801c3a7620b7dc8e0",
    "measurementId": "G-360QX46885",
    "databaseURL": "https://tfgapp-385f5-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


@login_required
def buscar_duenho(request):
    mensaje = ''
    duenhos = None
    if request.method == 'POST':
        cedula = request.POST.get('ci')
        duenhos = Usuario.objects.filter(ci=cedula)
        if not duenhos.exists():
            mensaje = 'No se encontraron dueños con esa cédula.'
    return render(request, 'mascotas/buscar.html', {'duenhos': duenhos, 'mensaje': mensaje})

# filtrar por cedula del usuario
@login_required
def ver_mascotas(request, cedula):
    # Filtrar las mascotas asociadas al usuario con la cédula proporcionada
    mascotas = Mascota.objects.filter(usuario__ci=cedula) # el doble guion bajo es para acceder a los campos de la tabla relacionada
    return render(request, 'mascotas/ver_mascotas.html', {'mascotas': mascotas})

@api_view(['POST'])
def registrar_mascota(request):
    if request.method == 'POST':
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            usuario = request.user  # El objeto User del usuario autenticado
            serializer = MascotaSerializer(data=request.data) # Se crea un serializador con los datos de la petición
            if serializer.is_valid():
                archivo_imagen = request.FILES.get('imagen') # Se obtiene la imagen de la petición
                if archivo_imagen:
                    nombre_archivo = f'mascotas/{uuid.uuid4()}.{archivo_imagen.name.split(".")[-1]}' # Se genera un nombre único para la imagen
                    imagen_url = storage.child(nombre_archivo).put(archivo_imagen)
                    serializer.save(usuario=usuario, imagen_url=imagen_url['downloadTokens']) # Se guarda la mascota en la base de datos
                    return Response(serializer.data, status=status.HTTP_201_CREATED)# Se responde con los datos de la mascota creada
                else:
                    return Response({'error': 'No se proporcionó ninguna imagen'}, status=status.HTTP_400_BAD_REQUEST)# Se responde con un error si no se proporcionó ninguna imagen
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)# Se responde con los errores del serializador si no es válido
        else:
            return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)  # Se responde con un error si el usuario no está autenticado
