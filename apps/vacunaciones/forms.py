from django import forms
from .models import Vacunacion

class FormVacunacion(forms.ModelForm):
    class Meta:
        model = Vacunacion
        fields = ['mascota', 'vacuna', 'dosis_aplicada', 'veterinario', 'fecha_vacunacion', 'fecha_proxima_vacunacion']