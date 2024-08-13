from django.db import models
from apps.especies.models import Especie
from apps.index.models import Usuario
# Create your models here.

class Recomendacion(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'recomendaciones'