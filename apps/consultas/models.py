from django.db import models
from apps.mascotas.models import Mascota

# Create your models here.
class Consulta(models.Model):
    fecha_consulta = models.DateField()
    motivo = models.CharField(max_length=100)
    indicacion = models.TextField(null=True, blank=True)
    veterinario = models.CharField(max_length=100)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'consultas'
        