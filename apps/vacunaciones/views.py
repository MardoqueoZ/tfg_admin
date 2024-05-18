from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from apps.mascotas.models import Mascota
from rest_framework import status
from django.urls import reverse
from .models import Vacunacion
from .forms import FormVacunacion
from .serializers import VacunacionSerializer

# Create your views here.

# lista de vacunaciones
@login_required
def vacunaciones(request, mascota_id):
    # Obtener la mascota o devolver un error 404 si no existe
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    # Obtener la cédula del usuario asociado a la mascota
    cedula_usuario = mascota.usuario.ci

    # Filtrar las vacunaciones para mostrar solo las de la mascota específica
    vacunaciones = Vacunacion.objects.filter(mascota=mascota)

    # Generar la URL de regreso con la cédula del usuario como argumento
    url_regreso = reverse('ver_mascotas', kwargs={'cedula': cedula_usuario})

    return render(request, 'vacunaciones/index.html', {'vacunaciones': vacunaciones, 'mascota': mascota, 'url_regreso': url_regreso})


# crear una vacunación
@login_required
def crear_vacunacion(request, mascota_id):
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormVacunacion(request.POST)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Asigna la instancia de la mascota al formulario antes de guardarlo
            vacunacion = form.save(commit=False)
            vacunacion.mascota = mascota
            vacunacion.save()
            
            return redirect('vacunaciones', mascota_id=mascota_id)
        else:
            print(form.errors)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la mascota
        form = FormVacunacion(initial={'mascota': mascota})

    return render(request, 'vacunaciones/crear.html', {'form': form, 'mascota': mascota})


# editar vacunacion
@login_required
def editar_vacunacion(request, vacunacion_id, mascota_id):
    # Obtén la instancia de la vacunación con el ID proporcionado o muestra un error 404 si no existe
    vacunacion = get_object_or_404(Vacunacion, pk=vacunacion_id)
    
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormVacunacion(request.POST, instance=vacunacion)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Guarda el formulario
            form.save()
            return redirect('vacunaciones', mascota_id=mascota_id)
        else:
            print(form.errors)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la vacunación
        form = FormVacunacion(instance=vacunacion)

    # Genera la URL de regreso
    url_regreso = reverse('vacunaciones', kwargs={'mascota_id': mascota_id})

    return render(request, 'vacunaciones/editar.html', {'form': form, 'vacunacion': vacunacion, 'mascota': mascota, 'url_regreso': url_regreso})

# eliminar vacunacion
@login_required
# eliminar vacunacion
def eliminar_vacunacion(request, vacunacion_id, mascota_id):
    # Obtiene la instancia con el ID proporcionado o muestra un error 404 si no existe
    vacunacion = get_object_or_404(Vacunacion, pk=vacunacion_id)
    
    # Elimina la instancia y redirige a la lista
    vacunacion.delete()
    return redirect('vacunaciones', mascota_id=mascota_id)


# APIS
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
        