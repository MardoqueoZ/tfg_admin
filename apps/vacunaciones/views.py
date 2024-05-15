from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.mascotas.models import Mascota
from django.urls import reverse
from .models import Vacunacion
from .forms import FormVacunacion

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