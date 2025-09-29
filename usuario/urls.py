# cuentas/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import PerfilUsuarioUpdateView, CambiarContrasenaView

app_name = 'usuario'

urlpatterns = [
    path('perfil/', PerfilUsuarioUpdateView.as_view(), name='editar_perfil'),
    path('cambiar-contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
