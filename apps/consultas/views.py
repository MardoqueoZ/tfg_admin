from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from apps.consultas.serializers import ConsultaSerializer
from apps.mascotas.models import Mascota
from .models import Consulta
from .forms import FormConsulta

# Create your views here.

# lista de consultas
@login_required
def consultas(request, mascota_id):
    # Obtener la mascota o devolver un error 404 si no existe
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    # Obtener la cédula del usuario asociado a la mascota
    cedula_usuario = mascota.usuario.ci

    # Filtrar los tratamientos para mostrar solo las de la mascota específica
    consultas = Consulta.objects.filter(mascota=mascota)

    # Generar la URL de regreso con la cédula del usuario como argumento
    url_regreso = reverse('ver_mascotas', kwargs={'cedula': cedula_usuario})

    return render(request, 'consultas/index.html', {'consultas': consultas, 'mascota': mascota, 'url_regreso': url_regreso})

# crear consulta
@login_required
def crear_consulta(request, mascota_id):
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=mascota_id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormConsulta(request.POST)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Asigna la instancia de la mascota al formulario antes de guardarlo
            consulta = form.save(commit=False)
            consulta.mascota = mascota
            consulta.save()
            
            return redirect('consultas', mascota_id=mascota_id)
        else:
            print(form.errors)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la mascota
        form = FormConsulta(initial={'mascota': mascota})

    return render(request, 'consultas/crear.html', {'form': form, 'mascota': mascota})

# editar consulta
@login_required
def editar_consulta(request, consulta_id, mascota_id):
    # Obtén la instancia de la consulta con el ID proporcionado o muestra un error 404 si no existe
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    # Obtén la instancia de la mascota
    mascota = consulta.mascota

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormConsulta(request.POST, instance=consulta)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Asigna la instancia de la mascota al formulario antes de guardarlo
            consulta = form.save(commit=False)
            consulta.mascota = mascota
            consulta.save()
            
            return redirect('consultas', mascota_id=mascota_id)
        else:
            print(form.errors)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la mascota
        form = FormConsulta(instance=consulta)
        
    # Genera la URL de regreso
    url_regreso = reverse('consultas', kwargs={'mascota_id': mascota_id})

    return render(request, 'consultas/editar.html', {'form': form, 'consulta': consulta, 'mascota': mascota, 'url_regreso': url_regreso})


# ver consulta
@login_required
def ver_consulta(request, consulta_id, mascota_id):
    # Obtén la instancia de la consulta con el ID proporcionado o muestra un error 404 si no existe
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    # Genera la URL de regreso
    url_regreso = reverse('consultas', kwargs={'mascota_id': mascota_id})

    return render(request, 'consultas/ver.html', {'consulta': consulta, 'url_regreso': url_regreso})

# eliminar consulta
@login_required
def eliminar_consulta(request, consulta_id, mascota_id):
    # Obtén la instancia de la consulta con el ID proporcionado o muestra un error 404 si no existe
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    
    # Elimina la consulta
    consulta.delete()
    
    return redirect('consultas', mascota_id=mascota_id)
    

# api listado de consultas
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_consultas(request, mascota_id) -> Response:
    # obtener las consultas de la mascota
    consultas = Consulta.objects.filter(mascota__id=mascota_id).values('id', 'fecha', 'motivo', 'indicacion', 'veterinario', 'mascota')
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