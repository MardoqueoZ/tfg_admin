from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from django import forms
from django.contrib.auth.models import Group

class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ('username' ,'password')
        

class FormCambioRol(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.all()
