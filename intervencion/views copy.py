from django.shortcuts import render


# Create your views here.

from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from .forms import IntervencionForm
from .models import Intervencion
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class IntervencionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Intervencion
    template_name = "intervencion/intervencion_crear.html"
    form_class = IntervencionForm
    success_url = reverse_lazy('core:index')
    context_object_name = 'intervenciones'
    login_url = 'core:login'
    permission_required = 'intervencion.puede_crear_intervencion'  # reemplaza 'intervencion' por tu app_label
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso

    # Opcional: manejar 403 de forma personalizada
    def handle_no_permission(self):
        return render(self.request, 'core/403.html', status=403)
    


def listar_intervenciones(request):
    intervenciones = Intervencion.objects.all()
    next_url = request.GET.get("next")       # para redirigir después

    return render(request, "intervencion/intervecion_agregar.html",{ 
        "intervenciones": intervenciones,
        "next_url": next_url,   # lo mandamos al template
    })