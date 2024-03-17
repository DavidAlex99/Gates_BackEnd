from rest_framework import serializers
from .models import Medico, Perfil, ImagenPerfil, Servicio, Contacto, ImagenContacto, Paciente
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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

class ImagenContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenContacto
        fields = ('imagen', 'created', 'updated')


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

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = ['id', 'username', 'email', 'password'] 
        extra_kwargs = {'password': {'write_only': True}} 
    def create(self, validated_data): 
        user = User.objects.create_user( 
            validated_data['username'], 
            email=validated_data['email'], 
            password=validated_data['password'] ) 
        return user 

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['nombre']