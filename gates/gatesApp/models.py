from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.IntegerField()


# ubicacion del consultorio
class Ubicacion(models.Model):
    direccion = models.CharField(max_length=255)
    direccion_secundaria = models.CharField(max_length=255, blank=True, null=True)

class Consultorio(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    especialidad = models.CharField(max_length=100)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class Servicio(models.Model):
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def agregar_contacto(self):
        pass    