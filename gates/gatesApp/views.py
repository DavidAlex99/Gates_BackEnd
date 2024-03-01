from django.shortcuts import render, HttpResponse, redirect
from .forms import ServicioForm, ContactoForm, SobreNosForm, UbicacionForm, MedicoForm
from .models import Servicio, Contacto, Medico
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# La vista personalizada para el inicio de sesión
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm  # Asegúrate de tener un CustomLoginForm o puedes usar el predeterminado
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})

# La vista del perfil de usuario
@login_required
def user_profile(request, username):
    # Asegúrate de que el nombre de usuario en la URL coincida con el usuario logueado
    if username != request.user.username:
        return redirect('user_profile', username=request.user.username)
    return render(request, 'user_profile.html', {'username': username})

# La vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def crear_medico(request, username):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    if request.method == 'POST':
        formulario_servicio = MedicoForm(request.POST, request.FILES)
        if formulario_servicio.is_valid():
            medico = formulario_servicio.save(commit=False)
            medico.usuario = request.user  # Asigna el usuario actual al objeto medico
            medico.save()
            return redirect('Servicios', username=username)  # Reemplaza con el nombre real de la vista
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = MedicoForm()
    return render(request, 'crear_medico.html', {'miFormularioMedico': formulario_servicio})

def home(request):
    return render(request, "home.html")

# vista para el menu
def servicios(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    # aqui se renderizaran los servicios de la base de datos
    servicios = Servicio.objects.all()
    return render(request, "servicios.html", {"servicios": servicios})

# vista para el menu
def subirServicio(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = ServicioForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Servicios', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ServicioForm()
    return render(request, "subirServicio.html", {'formulario_servicio': formulario_servicio})

# vista para Sobre Nosotros
def acerca(request, username):
# Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = SobreNosForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Acerca', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = SobreNosForm()
    return render(request, "acerca.html", {'miFormularioSobreNos': formulario_servicio})

#vista para el contacto
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactoForm
from .models import Contacto, Medico

def contacto(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    medico = get_object_or_404(Medico, usuario=request.user)
    # Intenta obtener el contacto existente del médico.
    # Si no existe, crea uno nuevo sin guardarlo aún en la base de datos.
    contacto, created = Contacto.objects.get_or_create(medico=medico, defaults={})
    
    if request.method == "POST":
        form = ContactoForm(request.POST, request.FILES, instance=contacto)
        if form.is_valid():
            contacto = form.save(commit=False)
            # Asegúrate de que el campo teléfono se establezca adecuadamente
            if not contacto.telefono:
                contacto.telefono = 'Algún valor por defecto o lógica para asignar un teléfono'
            contacto.save()
            return redirect('Home', username=username)
    else:
        form = ContactoForm(instance=contacto)

    return render(request, "contacto.html", {
        'form': form,
        'contacto': contacto,
        'created': created
    })

#vista para la ubicacion
def ubicacion(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = UbicacionForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = UbicacionForm()
    return render(request, "ubicacion.html", {'miFormularioUbicacion': formulario_servicio})

# vista para el calendario
def calendario(request):
    return render(request, "calendario.html")

