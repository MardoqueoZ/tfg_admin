from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegisterForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username' ,'ci','email', 'password1', 'password2')
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ('username' ,'password')
        