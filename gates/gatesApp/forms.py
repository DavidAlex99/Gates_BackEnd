from django import forms
from .models import Servicio, Contacto, ImagenContacto, Perfil, ImagenPerfil, Medico, Cita
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# formulario personalizado para el inicio de sesion
class CustomMedicoLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
# formulario para muestreo para actualizar informacion como 
# nobre, edad desues de registrar
class MedicoRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Ingrese su email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'edad', 'imagen', 'especialidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
        }



class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['estado', 'fecha_hora_inicio', 'fecha_hora_fin', 'motivo_consulta', 'notas']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_hora_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'precio', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['descripcion', 'direccion', 'direccion_secundaria', 'correo', 'telefono', 'latitud', 'longitud']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_secundaria': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            # campos que se va usar para la api de google maps
            'latitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ImagenContactoForm(forms.ModelForm):
    class Meta:
        model = ImagenContacto
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

ImagenContactoFormSet = inlineformset_factory(
    Contacto, ImagenContacto, 
    form=ImagenContactoForm, 
    extra=4,  # Cambiado de 4 a 0 para no mostrar formularios extras por defecto.
    can_delete=True,  # Permite marcar imágenes para eliminar.
)

    
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['descripcion', 'titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ImagenPerfilForm(forms.ModelForm):
    class Meta:
        model = ImagenPerfil
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

ImagenPerfilFormSet = inlineformset_factory(
    Perfil, ImagenPerfil, 
    form=ImagenPerfilForm, 
    extra=4,  # Puedes ajustar el número de formularios extra que quieres mostrar.
    can_delete=True,  # Permite marcar imágenes para eliminar.
)

