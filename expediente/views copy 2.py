from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import ListView, CreateView
from .models import Expediente
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages



from django.views.generic import FormView
from .forms import MedioIngresoForm, ExpedienteCompletoForm
from .models import Expediente, ExpedientePersona



class ExpedienteListView(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expediente/expediente_list.html'
    context_object_name = 'expedientes'
    login_url = 'core:login'

    def get_queryset(self):
        return Expediente.objects.all().order_by('identificador')
    



class SeleccionarMedioIngresoView(FormView):
    template_name = "expediente/seleccionar_medio_ingreso.html"
    form_class = MedioIngresoForm

    def form_valid(self, form):
        self.request.session['medio_ingreso_id'] = form.cleaned_data['medio_ingreso'].id
        return redirect('expediente:expediente_crear')


class ExpedienteCreateView(FormView):
    template_name = "expediente/expediente_form.html"
    form_class = ExpedienteCompletoForm
    success_url = reverse_lazy('expediente_lista')

    def get_initial(self):
        initial = super().get_initial()
        medio_ingreso_id = self.request.session.get('medio_ingreso_id')
        if medio_ingreso_id:
            initial['medio_ingreso'] = medio_ingreso_id
        return initial

    def form_valid(self, form):
        medio_ingreso_id = self.request.session.get('medio_ingreso_id')
        if not medio_ingreso_id:
            return redirect('seleccionar_medio_ingreso')

        # Guardar expediente
        expediente = form.save(commit=False)
        expediente.medio_ingreso_id = medio_ingreso_id
        expediente.save()

        # Guardar relación expediente-persona
        ExpedientePersona.objects.create(
            expediente=expediente,
            persona=form.cleaned_data['persona'],
            rol=form.cleaned_data['rol']
        )

        return redirect(self.success_url)
