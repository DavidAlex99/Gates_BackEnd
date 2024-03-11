from django.shortcuts import render, redirect, get_object_or_404
from .forms import MedicoForm, UserRegisterForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Medico
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'
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



