from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


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

