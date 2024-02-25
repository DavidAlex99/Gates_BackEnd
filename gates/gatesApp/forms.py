from django import forms
from .models import Servicio, Ubicacion, Contacto

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
        model: Contacto
        fields = ['medico', 'correo', 'telefono', 'imagen']

