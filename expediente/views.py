# views.py
import datetime
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import redirect
from .forms import DemandaEspontanea, MedioIngresoForm, OficioForm
from .models import Expediente, ExpedientePersona, Rol, ExpedienteInstitucion, MedioIngreso


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

    def get_initial(self):
        initial = super().get_initial()
        initial['medio_ingreso'] = 1  # ID por defecto
        return initial
    
    
    #def form_valid(self, form):
        #medio_ingreso_id = form.cleaned_data['medio_ingreso'].id
        # Redirige al formulario de expediente pasando el id del medio de ingreso
        #return redirect('expediente:expediente_create_with_medio', medio_id=medio_ingreso_id)
    
    def form_valid(self, form):
        medio_ingreso_id = form.cleaned_data['medio_ingreso'].id

        if medio_ingreso_id in [1,] :
            return redirect('expediente:expediente_create_with_medio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [2,3, 4, 5, 6] :
            return redirect('expediente:expediente_create_oficio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [7,] :
            return redirect('expediente:expediente_create_oficio', medio_id=medio_ingreso_id)
        else:
            return redirect('expediente:medio_ingreso_select')



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
            initial['fecha_creacion'] = datetime.date.today
        return initial

    #Función del formulario para obtener usuario y medio de ingreso
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form

    def form_valid(self, form):
        persona = form.cleaned_data['persona']
        sede = form.cleaned_data['sede']
        fecha_creacion = form.cleaned_data['fecha_creacion']
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
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,
            tipo_solicitud=tipo_solicitud,
            estado_expediente=estado_expediente,
            grupo_etario=grupo_etario,
            edad_persona=edad_persona,
            situacion_habitacional_hist=situacion_habitacional_hist,
            resumen_intervencion=resumen_intervencion,
            observaciones=observaciones,
        )
        expediente.save()  # Identificador generado automáticamente

        #rol, _ = Rol.objects.get_or_create(rol='Paciente')  # 
        rol = Rol.objects.get(pk=1)
        ExpedientePersona.objects.create(
            expediente=expediente,
            persona=persona,
            rol=rol
        )

        return super().form_valid(form)
    
    
    
class OficioCreateView(FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.kwargs.get('medio_id')
        if medio_id:
            initial['medio_ingreso'] = medio_id
            initial['fecha_creacion'] = datetime.date.today
        return initial

    #Función del formulario para obtener usuario y medio de ingreso
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form

    def form_valid(self, form):
        institucion = form.cleaned_data['institucion']
        fecha_de_juzgado = form.cleaned_data['fecha_de_juzgago']
        fecha_de_recepcion = form.cleaned_data['fecha_de_recepcion']
        persona = form.cleaned_data['persona']
        sede = form.cleaned_data['sede']
        fecha_creacion = form.cleaned_data['fecha_creacion']
        medio_ingreso = form.cleaned_data['medio_ingreso']
        tipo_solicitud = form.cleaned_data['tipo_solicitud']
        estado_expediente = form.cleaned_data['estado_expediente']
        grupo_etario = form.cleaned_data['grupo_etario']
        edad_persona = form.cleaned_data['edad_persona']
        situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        resumen_intervencion = form.cleaned_data['resumen_intervencion']
        expediente_fisico = form.cleaned_data['expediente_fisico']
        clave_sisfe = form.cleaned_data['clave_sisfe']
        cuij = form.cleaned_data['cuij']
        observaciones = form.cleaned_data['observaciones']

        expediente = Expediente(
            institucion = institucion,
            fecha_de_juzgado = fecha_de_juzgado,
            fecha_de_recepcion = fecha_de_recepcion,
            persona = persona,
            sede = sede,
            fecha_creacion = fecha_creacion,
            medio_ingreso = medio_ingreso,
            tipo_solicitud = tipo_solicitud,
            estado_expediente = estado_expediente,
            grupo_etario = grupo_etario,
            edad_persona = edad_persona,
            situacion_habitacional_hist = situacion_habitacional_hist,
            resumen_intervencion = resumen_intervencion,
            expediente_fisico = expediente_fisico,
            clave_sisfe = clave_sisfe,
            cuij = cuij,
            observaciones = observaciones,

        )
        expediente.save()  # Identificador generado automáticamente

        #rol, _ = Rol.objects.get_or_create(rol='Paciente')  # 
        rol = Rol.objects.get(pk=1)
        ExpedienteInstitucion.objects.create(
            expediente=expediente,
            institucion=institucion,
            rol=rol
        )

        return super().form_valid(form)