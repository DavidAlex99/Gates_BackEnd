from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicoForm, UserRegisterForm, ContactoForm, ImagenContactoFormSet
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Medico, Contacto
from django.contrib.auth.views import LoginView

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
