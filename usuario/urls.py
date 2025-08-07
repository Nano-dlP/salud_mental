# cuentas/urls.py
from django.urls import path
from .views import PerfilUsuarioUpdateView, CambiarContrasenaView

app_name = 'usuario'

urlpatterns = [
    path('perfil/', PerfilUsuarioUpdateView.as_view(), name='editar_perfil'),
    path('cambiar-contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
]
