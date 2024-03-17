from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicoForm, UserRegisterForm, ContactoForm, ImagenContactoFormSet, PerfilForm, ImagenPerfilFormSet, ImagenPerfilForm, ServicioForm
from .models import Medico, Contacto, Perfil, Servicio, Paciente
from django.contrib.auth import authenticate, login 

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from .serializers import MedicoSerializer, ServicioSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login 
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import CustomLoginForm
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseNotAllowed
import os
from django.contrib.auth.models import User
from itertools import groupby
from operator import attrgetter

# para serialiara  traves de la API
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response    
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login 
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
# fin para el registro de usuario

# para serializar comidas, eventos, get emprendimiento
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# fin para serializar  traves de la API



from django.forms import inlineformset_factory


class CustomLoginView(LoginView):
    template_name = 'login.html'
    # form_class = CustomLoginForm  # Asegúrate de definir este formulario si es necesario.
    redirect_authenticated_user = True

    def get_success_url(self):
        # Después de iniciar sesión, redirigimos al usuario a su página 'home'.
        return reverse('home', kwargs={'username': self.request.user.username})
    
# La vista de registro de usuarios y médicos
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            # Redirigir al usuario para añadir el perfil del médico después del registro.
            return redirect(reverse('add_medico_profile', kwargs={'username': user.username}))
    else:
        user_form = UserRegisterForm()
    return render(request, 'register.html', {'user_form': user_form})

@login_required
def user_profile(request, username):
    # Asegúrate de que el nombre de usuario en la URL coincida con el usuario logueado
    if username != request.user.username:
        return redirect('user_profile', username=request.user.username)
    return render(request, 'user_profile.html', {'username': username})

# visa para cerrar sesion
def logout_page(request):
    return render(request, 'logout_page.html')

@login_required
def home(request, username):
    # Asegúrate de que el nombre de usuario en la URL coincida con el usuario logueado
    if username != request.user.username:
        return redirect('home', username=request.user.username)
        # Intenta obtener el perfil del médico, si no existe, podría redirigir a la página de creación del perfil
    try:
        medico = Medico.objects.get(user__username=username)
    except Medico.DoesNotExist:
        return redirect('add_medico_profile', username=username)
    # Renderiza la página home con el contexto del médico
    return render(request, 'home.html', {'medico': medico})



# Vista para agregar perfil de médico
@login_required
def add_medico_profile(request, username):
    if request.user.username != username:
        return redirect('add_medico_profile', username=request.user.username)
    if request.method == 'POST':
        medico_form = MedicoForm(request.POST, request.FILES)
        if medico_form.is_valid():
            medico = medico_form.save(commit=False)
            medico.user = request.user
            medico.save()
            # Redirigir a la página de inicio del médico después de crear el perfil.
            return redirect('home', username=username)
    else:
        medico_form = MedicoForm()
    return render(request, 'medico_form.html', {'miFormularioMedico': medico_form})

@login_required
def subirPerfil(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        formset = ImagenPerfilFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            perfil = form.save(commit=False)
            perfil.medico = medico
            perfil.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.perfil = perfil
                instance.save()
            return redirect('perfilDetalle', username=username)
    else:
        form = PerfilForm()
        formset = ImagenPerfilFormSet()
    return render(request, 'perfilSubir.html', {
        'miFormularioPerfil': form,
        'miFormularioImagenesPerfil': formset,
        'medico': medico,
        'username': username,
    })


@login_required
def detallePerfil(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    perfil = get_object_or_404(Perfil, medico=medico)
    imagenes = perfil.imagenesPerfil.all()
    return render(request, 'perfilDetalle.html', {
        'perfil': perfil,
        'imagenes': imagenes,
        'medico': medico,
        'username': username,
    })

@login_required
def actualizarPerfil(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    perfil, created = Perfil.objects.get_or_create(medico=medico)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        formset = ImagenPerfilFormSet(request.POST, request.FILES, instance=perfil)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('perfilDetalle', username=username)
    else:
        form = PerfilForm(instance=perfil)
        formset = ImagenPerfilFormSet(instance=perfil)

    return render(request, 'perfilActualizar.html', {
        'miFormularioPerfil': form,
        'miFormularioImagenesPerfil': formset,
        'perfil': perfil,
        'medico': medico,
        'username': username,
    })

# srvicios
@login_required
def servicios(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    servicios_list = Servicio.objects.filter(medico=medico)

    return render(request, 'servicios.html', {
        'medico': medico,
        'username': username,
        'servicios_list': servicios_list,
    })

@login_required
def subirServicio(request, username):
    medico = get_object_or_404(Medico, user__username=username)

    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.medico = medico
            servicio.save()
            return redirect('servicios', username=username)
    else:
        # El campo 'emprendimiento' se establece automáticamente en la vista, oculto para el usuario.
        form = ServicioForm(initial={'medico': medico})
    
    return render(request, 'servicioSubir.html', {
        'username': username,
        'miFormularioServicio': form,
        'medico': medico
    })


@login_required
def detalleServicio(request, username, id):
    medico = get_object_or_404(Medico, user__username=username)
    servicio = get_object_or_404(Servicio, id=id, medico=medico)
    return render(request, 'servicioDetalle.html', {
        'servicio': servicio,
        'username': username,
        'medico': medico,
    })



@login_required
def actualizarServicio(request, username, id):
    medico = get_object_or_404(Medico, user__username=username)
    servicio = get_object_or_404(Servicio, id=id, medico=medico)
    
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicios', username=username)
    else:
        form = ServicioForm(instance=servicio)
    
    return render(request, 'servicioActualizar.html', {
        'username': username,
        'miFormularioServicio': form,
        'servicio': servicio,
        'medico': medico
    })
# fin servicios

@login_required
def contactoSubir(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        formset = ImagenContactoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            contacto = form.save(commit=False)
            contacto.medico = medico
            contacto.save()
            formset.instance = contacto
            formset.save()
            return redirect('contactoDetalle', username=username)
    else:
        form = ContactoForm()
        formset = ImagenContactoFormSet()
    return render(request, 'contactoSubir.html', {
        'miFormularioContacto': form,
        'miFormularioImagenesContacto': formset,
        'username': username,
    })

@login_required
def contactoDetalle(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    contacto = get_object_or_404(Contacto, medico=medico)
    imagenes = contacto.imagenesContacto.all()
    return render(request, 'contactoDetalle.html', {
        'contacto': contacto,
        'imagenes': imagenes,
        'medico': medico,
        'username': username,
    })

@login_required
def contactoActualizar(request, username):
    medico = get_object_or_404(Medico, user__username=username)
    contacto, created = Contacto.objects.get_or_create(medico=medico)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        formset = ImagenContactoFormSet(request.POST, request.FILES, instance=contacto)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('contactoDetalle', username=username)
    else:
        form = ContactoForm(instance=contacto)
        formset = ImagenContactoFormSet(instance=contacto)
    return render(request, 'contactoActualizar.html', {
        'miFormularioContacto': form,
        'miFormularioImagenesContacto': formset,
        'contacto': contacto,
        'medico': medico,
        'username': username,
    })

# PARTE API
# vista para hacer posible la vsta de los medicos
class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

# PASO 3: para el registro de clientes medicos
@api_view(['POST'])
def register(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        nombre = request.data.get('nombre', None)
        if nombre:
            Paciente.objects.create(user=user, nombre=nombre)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)  
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)