from django.db import models
from apps.vacunas.models import Vacuna
from apps.mascotas.models import Mascota
from apps.index.models import Usuario

# Create your models here.
class Vacunacion(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    vacuna = models.ForeignKey(Vacuna, on_delete=models.CASCADE)
    dosis_aplicada = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    veterinario = models.CharField(max_length=100, null=True, blank=True)
    fecha_vacunacion = models.DateField()
    fecha_proxima_vacunacion = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'vacunaciones'
        
    
    