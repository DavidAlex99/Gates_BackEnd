from django.shortcuts import render, HttpResponse

# Create your views here.

#
def home(request):
    return HttpResponse("Inicio")

# vista para el menu
def servicios(request):
    return HttpResponse("Servicios")

# vista para Sobre Nosotros
def acerca(request):
    return HttpResponse("Acerca")

#vista para el contacto
def contacto(request):
    return HttpResponse("Contacto")

#vista para la ubicacion
def ubicacion(request):
    return HttpResponse("Ubicacion")

# vista para la galeria
def calendario(request):
    return HttpResponse("Calendario")