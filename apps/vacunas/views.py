from django.shortcuts import render
from .models import Vacuna
from .forms import FormVacuna
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from apps.especies.models import Especie
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# vista vacunas
def vacunas(request):
    vacunas = Vacuna.objects.all()
    return render(request, 'vacunas/index.html', {'vacunas': vacunas})

# crear vacunas
@login_required
def crear_vacuna(request):
    especies = Especie.objects.all()
    if request.method == 'POST':
        form = FormVacuna(request.POST)
        if form.is_valid():
            nombre_vacuna = form.cleaned_data['nombre']
            if Vacuna.objects.filter(nombre=nombre_vacuna).exists():
                form.add_error('nombre', 'Ya existe una vacuna con este nombre.')
                return render(request, 'vacunas/crear.html', {'form': form})

            vacuna = form.save(commit=False)
            vacuna.usuario = get_user(request)
            vacuna.save()

            return redirect('vacunas')
    else:
        form = FormVacuna()

    return render(request, 'vacunas/crear.html', {'form': form, 'especies': especies})

# editar vacuna
def editar_vacuna(request, vacuna_id):
    # Intenta obtener la vacuna con el ID proporcionado
    try:
        vacuna = Vacuna.objects.get(id=vacuna_id)
    except ObjectDoesNotExist:
        # Si la noticia no existe, devuelve un error 404
        return HttpResponseNotFound("La noticia no existe")

    if request.method == 'POST':
        # Si la solicitud es un POST, crea un formulario con los datos de la solicitud
        form = FormVacuna(request.POST, instance=vacuna)
        if form.is_valid():
            # Si el formulario es válido, guarda la vacuna y redirige a la página de vacunas
            vacuna = form.save(commit=False)
            vacuna.usuario = get_user(request)
            vacuna.save()
            return redirect('noticias')
    else:
        # Si la solicitud no es un POST, crea un formulario con la instancia de la vacuna
        form = FormVacuna(instance=vacuna)
    
    # Renderiza el template de edición de noticia con el formulario y la instancia de la noticia en el contexto
    return render(request, 'vacunas/editar.html', {'form': form, 'vacuna': vacuna, 'especies': Especie.objects.all()})


# eliminar vacuna
def eliminar_vacuna(request, vacuna_id):
    # se obtiene la vacuna
    vacuna = Vacuna.objects.get(pk=vacuna_id)
    # se elimina la vacuna
    vacuna.delete()
    # se redirige a la vista vacunas
    return redirect('vacunas')
