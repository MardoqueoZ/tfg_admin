from django.shortcuts import render
from .models import Mascota
from django.contrib.auth.decorators import login_required
from apps.index.models import Usuario
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.request import Request
from .serializers import MascotaSerializer
from django.http import JsonResponse
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
    # nombre y apellido del usuario
    usuario = Usuario.objects.get(ci=cedula)
    return render(request, 'mascotas/ver_mascotas.html', {'mascotas': mascotas, 'usuario': usuario})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrar_mascota(request: Request) -> Response:
    if request.method == 'POST':
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            usuario = request.user  # El objeto User del usuario autenticado
            serializer = MascotaSerializer(data=request.data) # Se crea un serializador con los datos de la petición
            if serializer.is_valid():
                archivo_imagen = request.FILES.get('imagen') # Se obtiene la imagen de la petición
                if archivo_imagen:
                    nombre_archivo = f'mascotas/{uuid.uuid4()}.{archivo_imagen.name.split(".")[-1]}' # Se genera un nombre único para la imagen
                    storage.child(nombre_archivo).put(archivo_imagen)
                    imagen_url = storage.child(nombre_archivo).get_url(None)  # Obtener la URL de la imagen
                    serializer.save(usuario=usuario, imagen_url=imagen_url) # Se guarda la mascota en la base de datos
                    mascota_creada = serializer.instance  # Obtener la instancia de la mascota creada
                    return Response({'mascota_id': mascota_creada.id, 'imagen_url': imagen_url}, status=status.HTTP_201_CREATED)  # Se responde con el ID de la mascota creada y la URL de la imagen almacenada en Firebase
                else:
                    return Response({'error': 'No se proporcionó ninguna imagen'}, status=status.HTTP_400_BAD_REQUEST)# Se responde con un error si no se proporcionó ninguna imagen
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)# Se responde con los errores del serializador si no es válido
        else:
            return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)  # Se responde con un error si el usuario no está autenticado        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_mascotas(request: Request) -> Response:
    # obtener todas las mascotas del usuario autenticado con los campos nombre, especie, raza, sexo e imagen_url
    mascotas = Mascota.objects.filter(usuario=request.user).values('id','nombre', 'especie', 'raza', 'fecha_nacimiento', 'sexo', 'imagen_url', 'usuario')
    # Devolver las mascotas en formato JSON
    return JsonResponse(list(mascotas), safe=False)


# editar mascota api
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editar_mascota(request: Request, mascota_id: int) -> Response:
    if request.method == 'PUT':
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener la mascota a editar
            mascota = Mascota.objects.filter(id=mascota_id, usuario=request.user).first()
            if mascota:
                serializer = MascotaSerializer(mascota, data=request.data, partial=True)  # Se crea un serializador con los datos de la petición
                if serializer.is_valid():
                    archivo_imagen = request.FILES.get('imagen')
                    imagen_url = mascota.imagen_url  # Valor predeterminado
                    if archivo_imagen:
                        nombre_archivo = f'mascotas/{uuid.uuid4()}.{archivo_imagen.name.split(".")[-1]}'
                        storage.child(nombre_archivo).put(archivo_imagen)
                        imagen_url = storage.child(nombre_archivo).get_url(None)
                        serializer.save(imagen_url=imagen_url)
                    else:
                        serializer.save()
                    return Response({'mascota_id': mascota.id, 'imagen_url': imagen_url}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'No se encontró la mascota'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
# eliminar mascota api
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_mascota(request: Request, mascota_id: int) -> Response:
    if request.method == 'DELETE':
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener la mascota a eliminar
            mascota = Mascota.objects.filter(id=mascota_id, usuario=request.user).first()
            if mascota:
                mascota.delete()
                return Response({'message': 'Mascota eliminada correctamente'}, status=204)
            else:
                return Response({'error': 'No se encontró la mascota'}, status=404)
        else:
            return Response({'error': 'Usuario no autenticado'}, status=401)
    else:
        return Response({'error': 'Método no permitido'}, status=405)
