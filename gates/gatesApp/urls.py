"""
URL configuration for gates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# imortacion de las vistass
from gatesApp import views

from django.conf import settings
from django.conf.urls.static import static

# para el inicio de sesion
from django.contrib.auth.views import LoginView, LogoutView

# para poder serializar os elementos
from rest_framework.routers import DefaultRouter
from .views import MedicoViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'medicos', MedicoViewSet)
router.register(r'servicios', ServicioViewSet)

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('<username>/home/', views.home, name='home'),
    path('<username>/add_profile/', views.add_medico_profile, name='add_medico_profile'),
    path('logout/', views.logout_page, name='logout_page'),

    path('<username>/perfil/subir', views.subirPerfil, name='perfilSubir'),
    path('<username>/perfil/detalle', views.detallePerfil, name='perfilDetalle'),
    path('<username>/perfil/actualizar', views.actualizarPerfil, name='perfilActualizar'),

    path('<str:username>/servicios/', views.servicios, name='servicios'),
    path('<str:username>/servicios/subirServicio/', views.subirServicio, name='servicioSubir'),
    path('<str:username>/servicios/<int:id>/', views.detalleServicio, name='servicioDetalle'),
    path('<str:username>/servicios/<int:id>/actualizarServicio/', views.actualizarServicio, name='servicioActualizar'),

    path('<username>/contacto/subir', views.contactoSubir, name='contactoSubir'),
    path('<username>/contacto/detalle', views.contactoDetalle, name='contactoDetalle'),
    path('<username>/contacto/actualizar', views.contactoActualizar, name='contactoActualizar'),

    path('', include(router.urls)),
    # PASO 4: para el registro de usuario

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
