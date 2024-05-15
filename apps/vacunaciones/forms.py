from django import forms
from .models import Vacunacion
from apps.mascotas.models import Mascota
from datetime import date

class FormVacunacion(forms.ModelForm):
    vacuna = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': "Nombre de la vacuna",
                'class': 'form-control'
            }
        )
    )
    dosis_aplicada = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': "Ingrese la dosis en ml",
                'class': 'form-control'
            }
        )
    )
    veterinario = forms.CharField(
        max_length=100,
        label='Veterinario/a',
        widget=forms.TextInput(
            attrs={
                'placeholder': "Veterinaria/o",
                'class': 'form-control'
            }
        )
        
    )

    fecha_vacunacion = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'placeholder': "Fecha de vacunación",
                'class': 'form-control',
                
            }
        ),
    )

    class Meta:
        model = Vacunacion
        fields = ['vacuna', 'dosis_aplicada',"veterinario", 'fecha_vacunacion']

