from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import TratamientoSerializer

from apps.mascotas.models import Mascota
from .models import Tratamiento
from .forms import FormTratamiento
# Create your views here.

# lista de tratamientos
@login_required
def tratamientos(request, mascota_id):
    # Obtener la mascota o devolver un error 404 si no existe
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    # Obtener la cédula del usuario asociado a la mascota
    cedula_usuario = mascota.usuario.ci

    # Filtrar los tratamientos para mostrar solo las de la mascota específica
    tratamientos = Tratamiento.objects.filter(mascota=mascota)

    # Generar la URL de regreso con la cédula del usuario como argumento
    url_regreso = reverse('ver_mascotas', kwargs={'cedula': cedula_usuario})

    return render(request, 'tratamientos/index.html', {'tratamientos': tratamientos, 'mascota': mascota, 'url_regreso': url_regreso})

# crear tratamiento
@login_required
def crear_tratamiento(request, mascota_id):
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormTratamiento(request.POST)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Asigna la instancia de la mascota al formulario antes de guardarlo
            tratamiento = form.save(commit=False)
            tratamiento.mascota = mascota
            tratamiento.save()
            
            return redirect('tratamientos', mascota_id=mascota_id)
        else:
            print(form.errors)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la mascota
        form = FormTratamiento(initial={'mascota': mascota})

    return render(request, 'tratamientos/crear.html', {'form': form, 'mascota': mascota})


# editar tratamiento
@login_required
def editar_tratamiento(request, tratamiento_id, mascota_id):
    # Obtén la instancia del tratamiento con el ID proporcionado o muestra un error 404 si no existe
    tratamiento = get_object_or_404(Tratamiento, pk=tratamiento_id)
    
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormTratamiento(request.POST, instance=tratamiento)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Guarda el formulario
            form.save()
            return redirect('tratamientos', mascota_id=mascota_id)
        else:
            print(form.errors)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la vacunación
        form = FormTratamiento(instance=tratamiento)

    # Genera la URL de regreso
    url_regreso = reverse('tratamientos', kwargs={'mascota_id': mascota_id})
    
    return render(request, 'tratamientos/editar.html', {'form': form, 'tratamiento': tratamiento, 'mascota': mascota, 'url_regreso': url_regreso})

# detalle de tratamiento
@login_required
def ver_tratamiento(request, tratamiento_id, mascota_id):
    # Obtén la instancia de la vacunación con el ID proporcionado o muestra un error 404 si no existe
    tratamiento = get_object_or_404(Tratamiento, pk=tratamiento_id)
    
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    # Genera la URL de regreso
    url_regreso = reverse('tratamientos', kwargs={'mascota_id': mascota_id})
    
    return render(request, 'tratamientos/ver.html', {'tratamiento': tratamiento, 'mascota': mascota, 'url_regreso': url_regreso})

# eliminar tratamiento
def eliminar_tratamiento(request, tratamiento_id, mascota_id):
    # Obtiene la instancia con el ID proporcionado o muestra un error 404 si no existe
    tratamiento = get_object_or_404(Tratamiento, pk=tratamiento_id)
    
    # Elimina la instancia y redirige a la lista
    tratamiento.delete()
    return redirect('tratamientos', mascota_id=mascota_id)

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