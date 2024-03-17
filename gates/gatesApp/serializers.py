from rest_framework import serializers
from .models import Medico, Perfil, ImagenPerfil, Servicio, Contacto, ImagenContacto, Paciente
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# arreglado
class ImagenPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPerfil
        fields = ('imagen', 'created', 'updated')

# arreglado
class PerfilSerializer(serializers.ModelSerializer):
    imagenesPerfil = ImagenPerfilSerializer(many=True, read_only=True)

    class Meta:
        model = Perfil
        fields = ('titulo', 'descripcion', 'imagenesPerfil', 'created', 'updated')

# corregido
class ServicioSerializer(serializers.ModelSerializer):
    medico_id = serializers.ReadOnlyField(source='medico.id')
    
    class Meta:
        model = Servicio
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'created', 'updated', 'medico_id']

# corregido
class ImagenContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenContacto
        fields = ('imagen', 'created', 'updated')

# corregido
class ContactoSerializer(serializers.ModelSerializer):
    imagenesContacto = ImagenContactoSerializer(many=True, read_only=True)

    class Meta:
        model = Contacto
        fields = ['descripcion', 'direccion', 'correo', 'telefono', 'latitud', 'longitud', 'imagenesContacto', 'created', 'updated']

class MedicoSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)
    servicios = ServicioSerializer(source='servicio_set', many=True, read_only=True)
    contacto = ContactoSerializer(read_only=True)

    class Meta:
        model = Medico
        fields = ('nombre', 'descripcion', 'edad', 'imagen', 'especialidad', 'perfil', 'servicios', 'contacto', 'created', 'updated')

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