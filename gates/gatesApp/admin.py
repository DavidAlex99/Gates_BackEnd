from django.contrib import admin

# Register your models here.
from .models import Paciente, Ubicacion, Consultorio, Medico, Servicio

class PacienteAdmin(admin.ModelAdmin):

    readonly_fields=("created","updated")

class UbicacionAdmin(admin.ModelAdmin):

    readonly_fields=("created","updated")

class ConsultorioAdmin(admin.ModelAdmin):

    readonly_fields=("created","updated")

class MedicoAdmin(admin.ModelAdmin):

    readonly_fields=("created","updated")

class ServicioAdmin(admin.ModelAdmin):

    readonly_fields=("created","updated")

#regisrar alas tablas como las clases
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Ubicacion, UbicacionAdmin)
admin.site.register(Consultorio, ConsultorioAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Servicio, ServicioAdmin)