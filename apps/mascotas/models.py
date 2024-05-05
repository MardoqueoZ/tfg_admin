from django.db import models
from apps.especies.models import Especie
from apps.index.models import Usuario

# Create your models here.
class Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    sexo = models.CharField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='mascotas', null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'mascotas'