# views.py
import datetime
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import redirect
from .forms import DemandaEspontanea, MedioIngresoForm
from .models import Expediente, ExpedientePersona, Rol


class ExpedienteListView(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expediente/expediente_list.html'
    context_object_name = 'expedientes'
    login_url = 'core:login'

    def get_queryset(self):
        return Expediente.objects.all().order_by('identificador')
    

# Paso 1: Selección del Medio de Ingreso
class MedioIngresoSelectView(FormView):
    template_name = 'expediente/medio_ingreso.html'
    form_class = MedioIngresoForm

    def form_valid(self, form):
        medio_ingreso_id = form.cleaned_data['medio_ingreso'].id
        # Redirige al formulario de expediente pasando el id del medio de ingreso
        return redirect('expediente/crear/', medio_id=medio_ingreso_id)
    

# Paso 2: Formulario de Expediente con MedioIngreso preseleccionado
class DemandaEspontaneaCreateView(FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.kwargs.get('medio_id')
        if medio_id:
            initial['medio_ingreso'] = medio_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Hacemos que el campo MedioIngreso sea readonly
        form.fields['medio_ingreso'].disabled = True
        return form

    def form_valid(self, form):
        persona = form.cleaned_data['persona']
        sede = form.cleaned_data['sede']
        medio_ingreso = form.cleaned_data['medio_ingreso']
        tipo_solicitud = form.cleaned_data['tipo_solicitud']
        estado_expediente = form.cleaned_data['estado_expediente']
        grupo_etario = form.cleaned_data['grupo_etario']
        edad_persona = form.cleaned_data['edad_persona']
        situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        resumen_intervencion = form.cleaned_data['resumen_intervencion']
        observaciones = form.cleaned_data['observaciones']

        expediente = Expediente(
            sede=sede,
            medio_ingreso=medio_ingreso,
            tipo_solicitud=tipo_solicitud,
            estado_expediente=estado_expediente,
            grupo_etario=grupo_etario,
            edad_persona=edad_persona,
            situacion_habitacional=situacion_habitacional_hist,
            resumen_intervencion=resumen_intervencion,
            observaciones=observaciones
        )
        expediente.save()  # Identificador generado automáticamente

        rol_titular, _ = Rol.objects.get_or_create(nombre='Titular')
        ExpedientePersona.objects.create(
            expediente=expediente,
            persona=persona,
            rol=rol_titular
        )

        return super().form_valid(form)