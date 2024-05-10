from django.db import models
from apps.index.models import Usuario
from apps.especies.models import Especie

# Create your models here.
class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    lote = models.CharField(max_length=50)
    laboratorio = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'vacunas'
        
    def __str__(self):
        return self.nombre