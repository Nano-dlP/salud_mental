from django.shortcuts import render


# Create your views here.

from django.views.generic import FormView
from .forms import IntervencionForm
from .models import Intervencion
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class IntervencionFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'intervencion/intervencion_crear.html'
    form_class = IntervencionForm
    success_url = reverse_lazy('intervencion:intervencion_list')
    login_url = 'core:login'
    permission_required = 'intervencion.add_intervencion'
    raise_exception = True

    def get_initial(self):
        initial = super().get_initial()
        expediente_id = self.request.GET.get('expediente_id')
        if expediente_id:
            initial['expediente'] = expediente_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente_id = self.request.GET.get('expediente_id')
        context['expediente_id'] = expediente_id  # Pasa el ID al template
        if expediente_id:
            from expediente.models import Expediente
            try:
                expediente = Expediente.objects.get(pk=expediente_id)
                context['expediente_seleccionado'] = expediente  # Puedes mostrar datos del expediente
            except Expediente.DoesNotExist:
                context['expediente_seleccionado'] = None
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        Intervencion.objects.create(
            expediente=data['expediente'],
            profesional=data['profesional'],
            tipo_intervencion=data['tipo_intervencion'],
            fecha_intervencion=data['fecha_intervencion'],
            observacion=data.get('observacion', '')
        )
        return super().form_valid(form)



def listar_intervenciones(request):
    intervenciones = Intervencion.objects.all()
    next_url = request.GET.get("next")       # para redirigir después

    return render(request, "intervencion/intervencion_list.html",{ 
        "intervenciones": intervenciones,
        "next_url": next_url,   # lo mandamos al template
    })