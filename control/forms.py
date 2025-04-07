from django import forms
from .models import Alumno, Asistencia


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido']

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['alumno', 'fecha', 'presente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
