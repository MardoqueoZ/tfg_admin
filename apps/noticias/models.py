from django.db import models
from apps.index.models import Usuario

# Create your models here.


class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to='noticias', null=True, blank=True)
    foto_url = models.URLField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-fecha']
        db_table = 'noticias'

# clase para la auditoria de las noticias
class AuditoriaNoticia(models.Model):
    noticia_id = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    usuario_id = models.CharField(max_length=100)
    accion = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auditoria_noticias'