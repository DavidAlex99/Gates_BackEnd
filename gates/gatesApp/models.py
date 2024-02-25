from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class Consultorio(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    especialidad = models.CharField(max_length=100)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    Hora_estimacion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='servicios_images')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    
class Cita(models.Model):
    nombre = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    servicios = models.ManyToManyField(Servicio)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Calendario(models.Model):
    citas = models.ManyToManyField(Cita)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Contacto(models.Model):
    imagen = models.ImageField(upload_to='contacto')
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_contacto(self):
        pass