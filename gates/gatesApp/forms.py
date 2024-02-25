from django import forms
from .models import Servicio, Ubicacion, Contacto, SobreNos
from django.contrib.auth.forms import AuthenticationForm

# formulario personalizado para el inicio de sesion
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'precio', 'descripcion', 'Hora_estimacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'Hora_estimacion': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class UbicacionForm(forms.ModelForm):
    class Meta:
        model: Ubicacion
        fields = ['direccion', 'direccion_secundaria', 'imagen']

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['medico', 'correo', 'telefono', 'imagen']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'imasgen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class SobreNosForm(forms.ModelForm):
    class Meta:
        model = SobreNos
        fields = ['descrpcion', 'imagen']
        widgets = {
            'descrpcion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['direccion', 'direccion_secundaria', 'imagen']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_secundaria': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }