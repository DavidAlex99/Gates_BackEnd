from django.shortcuts import render, HttpResponse, redirect
from .forms import ServicioForm
from .models import Servicio


# Create your views here.

#
def home(request):
    return render(request, "home.html")

# vista para el menu
def servicios(request):
    # aqui se renderizaran los servicios de la base de datos
    servicios = Servicio.objects.all()
    return render(request, "servicios.html", {"servicios": servicios})

# vista para el menu
def subir(request):
    if request.method == "POST":
        formulario_servicio = ServicioForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ServicioForm()
    return render(request, "subir.html", {'miFormulario': formulario_servicio})

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

