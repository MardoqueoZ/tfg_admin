from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from apps.noticias.models import AuditoriaNoticia
from .forms import LoginForm, FormCambioRol
from django.contrib.auth import authenticate, login
from .models import AuditoriaUsuario, Usuario
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user:
                if user.is_superuser or Group.objects.get(name='administrador') in user.groups.all():
                    login(request, user)
                    next_page = request.GET.get('next', '')
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect('noticias')
                else:
                    messages.error(request, 'No tienes los permisos para acceder a esta página')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'inicio/index.html', {'login_form': login_form})


# Cierre de sesión
def logout(request):
    django_logout(request)
    return redirect('index')

    

# lista de usuarios
@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'inicio/usuarios.html', {'usuarios': usuarios})

# editar rol de usuario
@login_required
def editar_rol(request, usuario_id):
    usuario = Usuario.objects.get(pk=usuario_id)
    grupos = Group.objects.all()
    # Actualizar el rol del usuario
    if request.method == 'POST':
        form = FormCambioRol(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        grupo_actual = usuario.groups.first()
        form = FormCambioRol(instance=usuario, initial={'groups': grupo_actual})

    return render(request, 'inicio/editar_rol.html', {'form': form, 'usuario': usuario, 'grupos': grupos})

# Auditoría Usuario
@login_required
def auditoria_usuarios(request):
    registros_usuarios = AuditoriaUsuario.objects.all()
    context = {
        'registros_usuarios': registros_usuarios,
    }
    return render(request, "auditorias/auditoria_usuarios.html", context)