from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    ci = models.IntegerField(unique=True, null=True)
    telefono = models.CharField(max_length=10)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'usuarios'
        
        
class AuditoriaUsuario(models.Model):
    # usuario es el id del usuario
    usuario = models.CharField(max_length=100, null=True)
    nombre_usuario = models.CharField(max_length=100)
    grupo_usuario = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre_usuario
    
    class Meta:
        db_table = 'auditoria_usuarios'