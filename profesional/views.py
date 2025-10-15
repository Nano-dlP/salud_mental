from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
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


@login_required(login_url='core:login')
@permission_required('profesional.delete_profesional', login_url='core:login', raise_exception=True)
def desactivar_profesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    if profesional.estado:
        profesional.estado = False
        profesional.save()
        messages.success(request, "Profesional desactivado correctamente.")
        return redirect('profesional:profesional_list')
    else:
        profesional.estado = True
        profesional.save()
        messages.success(request, "Profesional activado correctamente.")
        return redirect('profesional:profesional_list')
    # Si es GET, muestra confirmación
    #return render(request, "institucion/confirmar_desactivacion.html", {"institucion": institucion})