from django import forms
from .models import Tratamiento

class FormTratamiento(forms.ModelForm):
        # nombre 
        nombre = forms.CharField(
            label='Tratamiento',
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del tratamiento'
                }
            )
        )
        
        # descripcion como textarea
        descripcion = forms.CharField(
            label='Descripción',
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion del tratamiento'
                }
            )
        )
        
        # fecha_inicio
        fecha_inicio = forms.DateField(
            label='Fecha de inicio',
            widget=forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Fecha de inicio del tratamiento'
                }
            )
        )
        
        # estado como select con las opciones de en curso, completado, cancelado
        estado = forms.CharField(
            label='Estado',
            widget=forms.Select(
                choices=[
                    ('En curso', 'En curso'),
                    ('Completado', 'Completado'),
                    ('Cancelado', 'Cancelado')
                ],
                attrs={
                    'class': 'form-control'
                }
            )
        )
        
        # veterinario
        veterinario = forms.CharField(
            label='Veterinario/a',
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del veterinario/a'
                }
            )
        )
        
        # fecha_fin, puede ser nulo
        fecha_fin = forms.DateField(
            label='Fecha de fin',
            required=False,
            widget=forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Fecha de fin del tratamiento'
                }
            )
        )
        class Meta:
            model = Tratamiento
            fields = ['nombre', 'descripcion', 'fecha_inicio', 'estado', 'veterinario', 'fecha_fin']