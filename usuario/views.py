# cuentas/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PerfilUsuarioForm
from django.contrib.auth import get_user_model
# cuentas/views.py (agrega esto también)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class PerfilUsuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = PerfilUsuarioForm
    template_name = 'usuario/usuario_edit.html'
    success_url = reverse_lazy('usuario:editar_perfil')  # redirige a sí misma
    permission_required = 'auth.change_user'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso

    def get_object(self, queryset=None):
        return self.request.user  # el usuario logueado

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)



class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'usuario/usuario_contrasenia.html'
    success_url = reverse_lazy('usuario:editar_perfil')
    permission_required = 'auth.change_user'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return super().form_valid(form)
