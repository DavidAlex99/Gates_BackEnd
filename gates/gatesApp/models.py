from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Medico(models.Model):
    ESPECIALIDAD = [
        ('CARDIOLOGO', 'Cardiologo'),
        ('PEDIATRA', 'Pediatra'),
        ('NEUROLOGO', 'Neurologo'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    edad = models.IntegerField()
    imagen = models.ImageField(upload_to='imagen_medico')
    especialidad = models.CharField(max_length=15, choices=ESPECIALIDAD, default='OTRO')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    # Otros campos y métodos relevantes para Medico...

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    
    # Otros campos y métodos relevantes para Paciente...

    def __str__(self):
        return self.nombre
    
# perfil del paciente
class Perfil(models.Model):
    titulo = models.TextField()
    descripcion = models.CharField(max_length=255)
    medico = models.OneToOneField(Medico, related_name='perfil', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

# multiples imagenes como tiitulos, displomas etc
class ImagenPerfil(models.Model):
    perfil = models.ForeignKey(Perfil, related_name='imagenesPerfil', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagen_perfil')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    

class Horario(models.Model):
    medico = models.ForeignKey(Medico, related_name='horarios', on_delete=models.CASCADE)
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Horario de {self.medico.nombre} el {self.dia} de {self.hora_inicio} a {self.hora_fin}"

class Cita(models.Model):
    ESTADO = [
        ('DISPONIBLE', 'Disponible'),
        ('CANCELADO', 'Cancelado'),
        ('EJECUTANDOSE', 'Ejecutandose'),
    ]

    medico = models.ForeignKey(Medico, related_name='citas', on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, related_name='citas', on_delete=models.SET_NULL, null=True, blank=True)
    horario = models.ForeignKey(Horario, related_name='citas', on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO, default='DISPONIBLE')
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    motivo_consulta = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    # Otros campos y métodos relevantes para Cita...

    def __str__(self):
        return f"Cita para {self.medico.nombre} el {self.fecha_hora_inicio.strftime('%Y-%m-%d %H:%M')}"
    

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.0)])
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagen_servicio')
    medico = models.ForeignKey(Medico, related_name='servicios', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def definir_precio(self, precio):
        self.precio = precio
        return self.save()
    
    # como aparecera en el panel de administracion
    def __str__(self):
        return self.nombre
    


# datos contacto van a estar apgados al consultorio
class Contacto(models.Model):
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    direccion_secundaria = models.CharField(max_length=255, blank=True, null=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20) 
    # campos que van a servir para el api google maps
    latitud = models.FloatField(null=True, blank=True)  # Nuevo campo para latitud
    longitud = models.FloatField(null=True, blank=True)  # Nuevo campo para longitud
    medico = models.OneToOneField(Medico, related_name='contacto', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

# multiples imagenes como lugares referenciales etc
class ImagenContacto(models.Model):
    contacto = models.ForeignKey(Contacto, related_name='imagenesContacto', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagen_contacto')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

