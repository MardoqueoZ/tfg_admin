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
from django.contrib.auth.models import Group
from django.contrib import messages
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from .serializers import UsuarioSerializer

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




# registro de usuario api, app flutter
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir el acceso sin autenticación
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
@permission_classes([AllowAny])  # Permitir el acceso sin autenticación
def login_api(request):
    usuario = get_object_or_404(Usuario, ci=request.data['ci'])
    if not usuario.check_password(request.data['password']):
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)
    # despues de verificar las credenciales, se crea o se obtiene el token de autenticacion
    token, _ = Token.objects.get_or_create(user=usuario)
    serializer = UsuarioSerializer(instance=usuario)
    return Response({"token": token.key, "usuario": serializer.data, "user_id": usuario.id, "message": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)


# cerrar sesion api, app flutter
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_api(request):
    request.auth.delete()
    return Response({'message': 'Cierre de sesión exitoso'}, status=status.HTTP_200_OK)


# Cierre de sesión
def logout(request):
    django_logout(request)
    return render(request, 'inicio/index.html')


    
