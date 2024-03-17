from rest_framework import serializers
from .models import Medico, Perfil, ImagenPerfil, Horario, Cita, Servicio, Contacto, ImagenContacto

class ImagenPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPerfil
        fields = ('imagen', 'created', 'updated')

class PerfilSerializer(serializers.ModelSerializer):
    imagenesPerfil = ImagenPerfilSerializer(many=True, read_only=True)

    class Meta:
        model = Perfil
        fields = ('titulo', 'descripcion', 'medico', 'imagenesPerfil', 'created', 'updated')

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)
    servicios = ServicioSerializer(many=True, read_only=True)
    contacto = ContactoSerializer(read_only=True)

    class Meta:
        model = Medico
        fields = ('user', 'nombre', 'descripcion', 'edad', 'imagen', 'especialidad', 'perfil', 'servicios', 'contacto', 'created', 'updated')
