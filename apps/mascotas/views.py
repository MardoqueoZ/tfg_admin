from django.shortcuts import render
from .models import Mascota
from django.contrib.auth.decorators import login_required
from apps.index.models import Usuario

@login_required
def buscar_duenho(request):
    mensaje = ''
    duenhos = None
    if request.method == 'POST':
        cedula = request.POST.get('ci')
        duenhos = Usuario.objects.filter(ci=cedula)
        if not duenhos.exists():
            mensaje = 'No se encontraron dueños con esa cédula.'
    return render(request, 'mascotas/buscar.html', {'duenhos': duenhos, 'mensaje': mensaje})

# filtrar por cedula del usuario
@login_required
def ver_mascotas(request, cedula):
    # Filtrar las mascotas asociadas al usuario con la cédula proporcionada
    mascotas = Mascota.objects.filter(usuario__ci=cedula) # el doble guion bajo es para acceder a los campos de la tabla relacionada
    # nombre y apellido del usuario
    usuario = Usuario.objects.get(ci=cedula)
    return render(request, 'mascotas/ver_mascotas.html', {'mascotas': mascotas, 'usuario': usuario})


