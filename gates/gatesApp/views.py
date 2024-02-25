from django.shortcuts import render, HttpResponse, redirect
from .forms import ServicioForm, ContactoForm, SobreNosForm, UbicacionForm
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
def subirServicio(request):
    if request.method == "POST":
        formulario_servicio = ServicioForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ServicioForm()
    return render(request, "subirServicio.html", {'formulario_servicio': formulario_servicio})

# vista para Sobre Nosotros
#def acerca(request, username):
def acerca(request, username):
# Asegúrate de que el usuario logueado es el mismo que el del URL.
    #if request.user.username != username:
        #return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = SobreNosForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            #return redirect('Acerca', username=username) 
            return redirect('Acerca')
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = SobreNosForm()
    return render(request, "acerca.html", {'miFormularioSobreNos': formulario_servicio})

#vista para el contacto
#def contacto(request, username):
def contacto(request):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    #if request.user.username != username:
        #return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = ContactoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            #return redirect('Home', username=username)
            return redirect('Home')  
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ContactoForm()
    return render(request, "contacto.html", {'miFormularioContacto': formulario_servicio})

#vista para la ubicacion
#def ubicacion(request, username):
def ubicacion(request):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    #if request.user.username != username:
        #return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = UbicacionForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            #return redirect('Home', username=username) 
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = UbicacionForm()
    return render(request, "ubicacion.html", {'miFormularioUbicacion': formulario_servicio})

# vista para la galeria
def calendario(request):
    return render(request, "calendario.html")

