from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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
    
