from django.shortcuts import render, redirect
from .models import Especie
from .forms import EspecieForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# especies
@login_required
def especies(request):
    especies = Especie.objects.all()
    return render(request, 'especies/index.html', {'especies': especies})

# crear especie
@login_required
def crear_especie(request):
    if request.method == 'POST':
        form = EspecieForm(request.POST)
        if form.is_valid():
            especie = form.save(commit=False)
            especie.save()
            return redirect('especies')
    else:
        form = EspecieForm()
    return render(request, 'especies/crear.html', {'form': form})

# editar especie
@login_required
def editar_especie(request, especie_id):
    especie = Especie.objects.get(id=especie_id)
    if request.method == 'GET':
        form = EspecieForm(instance=especie)
    else:
        form = EspecieForm(request.POST, instance=especie)
        if form.is_valid():
            form.save()
        return redirect('especies')
    return render(request, 'especies/editar.html', {'form': form, 'especie': especie})

# eliminar especie
@login_required
def eliminar_especie(request, especie_id):
    especie = Especie.objects.get(id=especie_id)
    especie.delete()
    return redirect('especies')
