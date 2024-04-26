from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse
from .forms import NoticiaForm
from django.contrib.auth import get_user
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Noticia
from django.core.exceptions import ObjectDoesNotExist
import os
import pyrebase

config = {
  "apiKey": "AIzaSyAKM1RT0QNYwYQfQ_bhoZk72urS6OK4PJE",
  "authDomain": "tfgapp-385f5.firebaseapp.com",
  "projectId": "tfgapp-385f5",
  "storageBucket": "tfgapp-385f5.appspot.com",
  "messagingSenderId": "53852604577",
  "appId": "1:53852604577:web:d4b78801c3a7620b7dc8e0",
  "measurementId": "G-360QX46885",
  "databaseURL": "https://tfgapp-385f5-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()



# Create your views here.
@login_required
def noticias(request):
    noticias = Noticia.objects.all()
    return render(request, 'noticias/index.html', {'noticias': noticias})

# crear noticias
# @login_required
# def crear_noticia(request):
#     if request.method == 'POST':
#         form = NoticiaForm(request.POST, request.FILES)
#         if form.is_valid():
#             noticia = form.save(commit=False)
#             noticia.usuario = get_user(request)
#             noticia.save()
#             return redirect('noticias')
#     else:
#         form = NoticiaForm()
#     return render(request, 'noticias/crear.html', {'form': form})

@login_required
def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.usuario = get_user(request)

            # Subir imagen a Firebase Storage en la carpeta "noticias"
            if 'foto' in request.FILES:
                foto = request.FILES['foto']
                storage.child("noticias").child(foto.name).put(foto)
                noticia.foto_url = storage.child("noticias").child(foto.name).get_url(None)

            noticia.save()
            return redirect('noticias')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear.html', {'form': form})

@login_required
def editar_noticia(request, noticia_id):
    # Intenta obtener la noticia con el ID proporcionado
    try:
        noticia = Noticia.objects.get(id=noticia_id)
    except ObjectDoesNotExist:
        # Si la noticia no existe, devuelve un error 404
        return HttpResponseNotFound("La noticia no existe")

    if request.method == 'POST':
        # Si la solicitud es un POST, crea un formulario con los datos de la solicitud
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            # Si el formulario es válido, guarda la noticia y redirige a la página de noticias
            noticia = form.save(commit=False)
            noticia.usuario = get_user(request)
            noticia.save()
            return redirect('noticias')
    else:
        # Si la solicitud no es un POST, crea un formulario con la instancia de la noticia
        form = NoticiaForm(instance=noticia)
    
    # Renderiza el template de edición de noticia con el formulario y la instancia de la noticia en el contexto
    return render(request, 'noticias/editar.html', {'form': form, 'noticia': noticia})


@login_required
def ver_noticia(request, noticia_id):
    # Intenta obtener la noticia con el ID proporcionado
    try:
        noticia = Noticia.objects.get(id=noticia_id)
    except ObjectDoesNotExist:
        # Si la noticia no existe, devuelve un error 404
        return HttpResponseNotFound("La noticia no existe")
    # Renderiza el template de ver noticia con la instancia de la noticia en el contexto
    return render(request, 'noticias/ver.html', {'noticia': noticia})
    
    
@login_required
def eliminar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)
    # Eliminar la foto
    noticia.foto.delete()
    # Eliminar la noticia
    noticia.delete()
    return redirect('noticias')


# apis
# obtener todas las noticias
def api_noticias(request):
    # obtener todas las noticias con los campos titulo, contenido, fecha y foto_url
    noticias = Noticia.objects.all().values('titulo', 'contenido', 'fecha', 'foto_url')
    # Devolver las noticias en formato JSON
    return JsonResponse(list(noticias), safe=False)