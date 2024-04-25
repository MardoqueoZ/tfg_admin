from django.db import models

# Create your models here.
class Especie(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'especies'