from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.
class Consultorio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Medico(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    especialidad = models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Paciente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edad = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

# ubicacion del consultorio
class Ubicacion(models.Model):
    imagen = models.ImageField(upload_to='imagen_ubicacion')
    direccion = models.CharField(max_length=255)
    direccion_secundaria = models.CharField(max_length=255, blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    Hora_estimacion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagen_servicio')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Calendario(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Cita(models.Model):
    nombre = models.CharField(max_length=100)
    #muchas citas pueden estar contenidas en un diccionario
    calendario = models.ForeignKey(Calendario, on_delete=models.CASCADE, related_name='citas_calendario')
    # una cita esta ligado a un paciente
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas_paciente')
    fecha_hora = models.DateTimeField()
    servicios = models.ManyToManyField(Servicio)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Contacto(models.Model):
    imagen = models.ImageField(upload_to='imagen_contacto')
    telefono = models.IntegerField(null=True, blank=True)
    correo = models.EmailField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_contacto(self):
        pass

class SobreNos(models.Model):
    descrpcion = models.TextField()
    imagen = models.ImageField(upload_to='imagen_sobre_nos')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_descripcion(self, descripcion):
        self.descrpcion = descripcion
        return self.save()