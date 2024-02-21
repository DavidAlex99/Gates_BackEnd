from django.shortcuts import render, HttpResponse

# Create your views here.

#
def home(request):
    return render(request, "home.html")

# vista para el menu
def servicios(request):
    return render(request, "servicios.html")

# vista para Sobre Nosotros
def acerca(request):
    return render(request, "acerca.html")

#vista para el contacto
def contacto(request):
    return render(request, "contacto.html")

#vista para la ubicacion
def ubicacion(request):
    return render(request, "ubicacion.html")

# vista para la galeria
def calendario(request):
    return render(request, "calendario.html")