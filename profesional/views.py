from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Profesional
from .forms import ProfesionalForm


class ProfesionalCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = "profesional/profesional_create.html"
    success_url = reverse_lazy("profesional:profesional_list")  # redirige al listado después de guardar
    login_url = 'core:login'
    permission_required = 'profesional.add_profesional'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso


class ProfesionalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Profesional
    template_name = "profesional/profesional_list.html"
    context_object_name = "profesionales"
    queryset = Profesional.objects.all().order_by('user__first_name', 'user__last_name')
    login_url = 'core:login'
    permission_required = 'profesional.view_profesional'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso


class ProfesionalUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = "profesional/profesional_create.html"
    success_url = reverse_lazy("profesional:profesional_list")
    login_url = 'core:login'
    permission_required = 'profesional.change_profesional'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso


class ProfesionalDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Profesional
    template_name = "profesional_confirm_delete.html"
    success_url = reverse_lazy("profesional:profesional_list")
    login_url = 'core:login'
    permission_required = 'profesional.delete_profesional'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso