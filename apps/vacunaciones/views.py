from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.mascotas.models import Mascota
from .models import Vacunacion
from .forms import FormVacunacion

# Create your views here.

# lista de vacunaciones
@login_required 
def vacunaciones(request, mascota_id):
    # Obtener la mascota o devolver un error 404 si no existe
    mascota = get_object_or_404(Mascota, pk=id)

    # Filtrar las vacunaciones para mostrar solo las de la mascota específica
    vacunaciones = Vacunacion.objects.filter(id=mascota_id)

    return render(request, 'vacunaciones/index.html', {'vacunaciones': vacunaciones, 'mascota': mascota})

# crear una vacunación
@login_required
def crear_vacunacion(request, mascota_id):
    # Obtén la instancia de la mascota
    mascota = get_object_or_404(Mascota, pk=id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormVacunacion(request.POST)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Asigna la mascota al formulario antes de guardarlo
            vacunacion = form.save(commit=False)
            vacunacion.mascota_id = mascota  # Asigna la instancia de la mascota, no solo el nombre
            vacunacion.save()
            
            return redirect('vacunaciones', id=mascota_id)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la mascota
        form = FormVacunacion(initial={'mascota_id': mascota})

    return render(request, 'vacunaciones/crear.html', {'form': form, 'mascota': mascota})

# editar una vacunación
@login_required
def editar_vacunacion(request, vacunacion_id, mascota_id):
    # Obtiene la instancia con el ID proporcionado o muestra un error 404 si no existe
    vacunacion = get_object_or_404(Vacunacion, pk=vacunacion_id)

    if request.method == 'POST':
        # Si la solicitud es de tipo POST, intenta procesar el formulario con los datos proporcionados
        form = FormVacunacion(request.POST, instance=vacunacion)

        # Verifica si el formulario es válido
        if form.is_valid():
            # Guarda el formulario
            form.save()
            return redirect('vacunaciones', id=mascota_id)
    else:
        # Si la solicitud es de tipo GET, crea un formulario con la instancia de la mascota
        form = FormVacunacion(instance=vacunacion)

    return render(request, 'vacunaciones/editar.html', {'form': form, 'vacunacion': vacunacion})

# eliminar vacunacion
@login_required
# eliminar vacunacion
def eliminar_vacunacion(request, vacunacion_id, mascota_id):
    # Obtiene la instancia con el ID proporcionado o muestra un error 404 si no existe
    vacunacion = get_object_or_404(Vacunacion, pk=vacunacion_id)
    
    # Elimina la instancia y redirige a la lista
    vacunacion.delete()
    return redirect('vacunaciones', id=mascota_id)