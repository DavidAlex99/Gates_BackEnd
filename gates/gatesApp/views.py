from django.shortcuts import render, HttpResponse

# Create your views here.

#
def home(request):
    return render(request, "gatesApp/home.html")

# vista para el menu
def servicios(request):
    return render(request, "gatesApp/servicios.html")

# vista para Sobre Nosotros
def acerca(request):
    return render(request, "gatesApp/acerca.html")

#vista para el contacto
def contacto(request):
    return render(request, "gatesApp/contacto.html")

#vista para la ubicacion
def ubicacion(request):
    return render(request, "gatesApp/ubicacion.html")

# vista para la galeria
def calendario(request):
    return render(request, "gatesApp/calendario.html")