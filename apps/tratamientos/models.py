from django.db import models
from apps.mascotas.models import Mascota

# Create your models here.

class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    estado = models.CharField(max_length=100)
    veterinario = models.CharField(max_length=100)
    fecha_fin = models.DateField(null=True, blank=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tratamientos'
        
    def __str__(self):
        return self.nombre 