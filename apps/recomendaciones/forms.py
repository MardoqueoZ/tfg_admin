from django import forms
from .models import Recomendacion

class RecomendacionForm(forms.ModelForm):
    class Meta:
        model = Recomendacion
        fields = ['nombre', 'contenido']