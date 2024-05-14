from django import forms
from .models import Vacuna
from apps.especies.models import Especie

class FormVacuna(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'descripcion', 'lote', 'fecha_vencimiento', 'laboratorio', 'especie']