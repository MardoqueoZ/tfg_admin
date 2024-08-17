from apps.index.models import Usuario
from apps.mascotas.models import Mascota
from apps.consultas.models import Consulta
from apps.especies.models import Especie
from apps.noticias.models import Noticia
from apps.recomendaciones.models import Recomendacion
from .serializers import *
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
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

# AUTENTICACIÓN
# registro de usuario api, app flutter
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir el acceso sin autenticación
def register_api(request):
    # Verificar si el usuario ya existe
    ci = request.data.get('ci')
    if Usuario.objects.filter(ci=ci).exists():
        return JsonResponse({'error': 'El usuario ya existe'}, status=status.HTTP_409_CONFLICT)
    
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        # Encriptar la contraseña antes de guardarla
        hashed_password = make_password(password)
        usuario = serializer.save(password=hashed_password)
        # Crear un token de autenticación para el nuevo usuario
        token = Token.objects.create(user=usuario)
        # registro exitoso
        return JsonResponse({'token': token.key, "usuario": serializer.data, "message": "Registro exitoso"}, status=status.HTTP_201_CREATED)
    

# iniciar sesion api, app flutter
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir el acceso sin autenticación
def login_api(request):
    usuario = get_object_or_404(Usuario, ci=request.data['ci'])
    if not usuario.check_password(request.data['password']):
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    # despues de verificar las credenciales, se crea o se obtiene el token de autenticacion
    token, _ = Token.objects.get_or_create(user=usuario)
    serializer = UsuarioSerializer(instance=usuario)
    return Response({"token": token.key, "usuario": serializer.data, "user_id": usuario.id, "message": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)

# cerrar sesion api, app flutter
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_api(request):
    request.auth.delete()
    return Response({'message': 'Cierre de sesión exitoso'}, status=status.HTTP_200_OK)


# ESPECIES
# obtener especie api
def api_especies(request):
    especies = Especie.objects.all().values('id','nombre')
    return JsonResponse(list(especies), safe=False)


# MASCOTAS
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
    

# NOTICIAS
# obtener todas las noticias
def api_noticias(request):
    # obtener todas las noticias con los campos titulo, contenido, fecha y foto_url
    noticias = Noticia.objects.all().values('titulo', 'contenido', 'fecha', 'foto_url')
    # Devolver las noticias en formato JSON
    return JsonResponse(list(noticias), safe=False)

# RECOMENDACIONES
def api_recomendaciones(request):
    # obtener todas las recomendaciones con los campos titulo, contenido y foto_url
    recomendaciones = Recomendacion.objects.all().values('nombre', 'contenido', 'especie', 'autor')
    # Devolver las recomendaciones en formato JSON
    return JsonResponse(list(recomendaciones), safe=False)
# TRATAMIENTOS.
# api lista de tratamientos
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_tratamientos(request, mascota_id) -> Response:
    # obtener los tratamientos de la mascota
    tratamientos = Tratamiento.objects.filter(mascota__id=mascota_id).values('id', 'nombre', 'descripcion', 'fecha_inicio', 'estado', 'veterinario', 'fecha_fin', 'mascota')
    # Devolver los tratamientos en formato JSON
    return JsonResponse(list(tratamientos), safe=False)

# api crear tratamiento
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_crear_tratamiento(request, mascota_id) -> Response:
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    if request.method == 'POST':
        # se crea un serializador con los datos de la petición
        serializer = TratamientoSerializer(data=request.data)
        if serializer.is_valid():
            # se guarda la vacunación en la base de datos
            serializer.save(mascota=mascota)
            tratamiento_creado = serializer.instance
            return Response({'trtamiento_id': tratamiento_creado.id, 'message': 'Registro de tratamiento exitoso'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# api editar tratamiento
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_editar_tratamiento(request, tratamiento_id, mascota_id) -> Response:
    if request.method == 'PUT':
        # Obtener el tratamiento a editar
        tratamiento = Tratamiento.objects.filter(id=tratamiento_id, mascota=mascota_id).first() # first retorna el primer objeto que cumpla con la condición
        if tratamiento:
            serializer = TratamientoSerializer(tratamiento, data=request.data, partial=True)  # Se crea un serializador con los datos de la petición
            if serializer.is_valid():
                serializer.save()
                return Response({'tratamiento_id': tratamiento.id, 'message': 'Actualización de tratamiento exitoso'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No se encontró el tratamiento'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# api eliminar tratamiento
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_eliminar_tratamiento(request, tratamiento_id, mascota_id) -> Response:
    if request.method == 'DELETE':
        # Obtener la vacunación a eliminar
        tratamiento = Tratamiento.objects.filter(id=tratamiento_id, mascota=mascota_id).first()
        if tratamiento:
            tratamiento.delete()
            return Response({'message': 'Eliminación de tratamiento exitoso'}, status=204)
        return Response({'error': 'No se encontró el tratamiento'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# VACUNACIONES
# api lista de vacunaciones
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_vacunaciones(request, mascota_id) -> Response:
    # obtener las vacunaciones de la mascota
    vacunaciones = Vacunacion.objects.filter(mascota__id=mascota_id).values('id', 'vacuna', 'dosis_aplicada', 'veterinario', 'fecha_vacunacion', 'mascota')
    # Devolver las vacunaciones en formato JSON
    return JsonResponse(list(vacunaciones), safe=False)

# api crear vacunacion
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_crear_vacunacion(request, mascota_id) -> Response:
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    if request.method == 'POST':
        # se crea un serializador con los datos de la petición
        serializer = VacunacionSerializer(data=request.data)
        if serializer.is_valid():
            # se guarda la vacunación en la base de datos
            serializer.save(mascota=mascota)
            vacunacion_creada = serializer.instance
            return Response({'vacunacion_id': vacunacion_creada.id, 'message': 'Registro de vacunacion exitoso'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# api editar vacunacion
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_editar_vacunacion(request, vacunacion_id, mascota_id) -> Response:
    if request.method == 'PUT':
        # Obtener la vacunación a editar
        vacunacion = Vacunacion.objects.filter(id=vacunacion_id, mascota=mascota_id).first()
        if vacunacion:
            serializer = VacunacionSerializer(vacunacion, data=request.data, partial=True)  # Se crea un serializador con los datos de la petición
            if serializer.is_valid():
                serializer.save()
                return Response({'vacunacion_id': vacunacion.id, 'message': 'Actualización de vacunación exitosa'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No se encontró la vacunación'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
# api eliminar vacunacion
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_eliminar_vacunacion(request, vacunacion_id, mascota_id) -> Response:
    if request.method == 'DELETE':
        # Obtener la vacunación a eliminar
        vacunacion = Vacunacion.objects.filter(id=vacunacion_id, mascota=mascota_id).first()
        if vacunacion:
            vacunacion.delete()
            return Response({'message': 'Eliminación de vacunación exitosa'}, status=204)
        return Response({'error': 'No se encontró la vacunación'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CONSULTAS
# api listado de consultas
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_consultas(request, mascota_id) -> Response:
    # obtener las consultas de la mascota
    consultas = Consulta.objects.filter(mascota__id=mascota_id).values('id', 'fecha_consulta', 'motivo', 'indicacion', 'veterinario', 'mascota')
    # Devolver las consultas en formato JSON
    return JsonResponse(list(consultas), safe=False)

# api crear consulta
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_crear_consulta(request, mascota_id) -> Response:
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    if request.method == 'POST':
        # se crea un serializador con los datos de la petición
        serializer = ConsultaSerializer(data=request.data)
        if serializer.is_valid():
            # se guarda la consulta en la base de datos
            serializer.save(mascota=mascota)
            consulta_creada = serializer.instance
            return Response({'consulta_id': consulta_creada.id, 'message': 'Registro de consulta exitosa'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# api editar consulta
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_editar_consulta(request, consulta_id, mascota_id) -> Response:
    if request.method == 'PUT':
        # Obtener la vacunación a editar
        consulta = Consulta.objects.filter(id=consulta_id, mascota=mascota_id).first()
        if consulta:
            serializer = ConsultaSerializer(consulta, data=request.data, partial=True)  # Se crea un serializador con los datos de la petición
            if serializer.is_valid():
                serializer.save()
                return Response({'consulta_id': consulta.id, 'message': 'Actualización de consulta exitosa'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No se encontró la consulta'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# api eliminar consulta
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_eliminar_consulta(request, consulta_id, mascota_id) -> Response:
    if request.method == 'DELETE':
        # Obtener la vacunación a eliminar
        consulta = Consulta.objects.filter(id=consulta_id, mascota=mascota_id).first()
        if consulta:
            consulta.delete()
            return Response({'message': 'Eliminación de consulta exitosa'}, status=204)
        return Response({'error': 'No se encontró la consulta'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)