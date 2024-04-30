from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as django_logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Usuario
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UsuarioSerializer

# Create your views here.

def index(request):
    register_form = RegisterForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                # Redirige al usuario a la página de inicio de sesión después del registro exitoso
                return redirect('index')
        elif 'login' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                # Autentica al usuario
                user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
                if user:
                    login(request, user)
                    # Redirige al usuario a la página deseada después del inicio de sesión
                    next_page = request.GET.get('next', '')
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect('noticias')

    return render(request, 'inicio/index.html', {'register_form': register_form, 'login_form': login_form})


# registro de usuario api, app flutter
@api_view(['POST'])
def register_api(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        # Encriptar la contraseña antes de guardarla
        hashed_password = make_password(password)
        usuario = serializer.save(password=hashed_password)
        usuario.save()
        # despues de guardar el usuario, se crea un token de autenticacion
        token = Token.objects.create(user=usuario)
        
        return JsonResponse({'token': token.key, "usuario": serializer.data, "message": "Registro exitoso"}, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# iniciar sesion api, app flutter
@api_view(['POST'])
def login_api(request):
    usuario = get_object_or_404(Usuario, ci=request.data['ci'])
    if not usuario.check_password(request.data['password']):
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)
    # despues de verificar las credenciales, se crea o se obtiene el token de autenticacion
    token, _ = Token.objects.get_or_create(user=usuario)
    serializer = UsuarioSerializer(instance=usuario)
    return Response({"token": token.key, "usuario": serializer.data, "message": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)


# cerrar sesion api, app flutter
@api_view(['POST'])
def logout_api(request):
    request.auth.delete()
    return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)


# Cierre de sesión
def logout(request):
    django_logout(request)
    return render(request, 'inicio/index.html')


    
