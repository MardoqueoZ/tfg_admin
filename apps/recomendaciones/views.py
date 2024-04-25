from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recomendacion
from .forms import RecomendacionForm
from django.contrib.auth import get_user

# Create your views here.

@login_required
def recomendaciones(request):
    recomendaciones = Recomendacion.objects.all()
    return render(request, 'recomendaciones/index.html', {'recomendaciones': recomendaciones})

# crear recomendacion
@login_required
def crear_recomendacion(request):
    if request.method == 'POST':
        form = RecomendacionForm(request.POST)
        if form.is_valid():
            recomendacion = form.save(commit=False)
            recomendacion.autor = get_user(request)
            recomendacion.save()
            return redirect('recomendaciones')
    else:
        form = RecomendacionForm()
    return render(request, 'recomendaciones/crear.html', {'form': form})

# editar recomendacion
@login_required
def editar_recomendacion(request, reco_id):
    recomendacion = Recomendacion.objects.get(id=reco_id)
    if request.method == 'POST':
        form = RecomendacionForm(request.POST, instance=recomendacion)
        if form.is_valid():
            form.save()
            return redirect('recomendaciones')
    else:
        form = RecomendacionForm(instance=recomendacion)
    return render(request, 'recomendaciones/editar.html', {'form': form, 'recomendacion': recomendacion})

# ver recomendacion
@login_required
def ver_recomendacion(request, reco_id):
    recomendacion = Recomendacion.objects.get(id=reco_id)
    return render(request, 'recomendaciones/ver.html', {'recomendacion': recomendacion})

# eliminar recomendacion
@login_required
def eliminar_recomendacion(request, reco_id):
    recomendacion = Recomendacion.objects.get(id=reco_id)
    recomendacion.delete()
    return redirect('recomendaciones')