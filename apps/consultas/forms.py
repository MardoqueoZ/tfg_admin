from django import forms
from apps.consultas.models import Consulta

class FormConsulta(forms.ModelForm):
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Fecha de la consulta'
            }
        )
    )
    
    # motivo como textarea
    motivo = forms.CharField(
        label='Motivo',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Motivo de la consulta'
            }
        )
    )
    
    # indicaciones como textarea
    indicacion = forms.CharField(
        label='Indicaciones',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Indicaciones de la consulta'
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
    
    class Meta:
        model = Consulta
        fields = ['fecha', 'motivo', 'indicacion', 'veterinario']
        