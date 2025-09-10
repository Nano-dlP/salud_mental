# views.py
import datetime
from django.views.generic import FormView
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import redirect
from .forms import DemandaEspontanea, MedioIngresoForm, OficioForm, SecretariaForm
from .models import Expediente, ExpedientePersona, Rol, ExpedienteInstitucion, ExpedienteDocumento, MedioIngreso
from persona.models import Persona

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ExpedienteDocumentoFormSet



class ExpedienteListView(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expediente/expediente_list.html'
    context_object_name = 'expedientes'
    login_url = 'core:login'

    def get_queryset(self):
        return Expediente.objects.all().order_by('identificador')
    

# Paso 1: Selección del Medio de Ingreso
class MedioIngresoSelectView(LoginRequiredMixin, FormView):
    template_name = 'expediente/medio_ingreso.html'
    form_class = MedioIngresoForm
    login_url = 'core:login'

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
        elif  medio_ingreso_id in [2, 3, 4, 5, 6] :
            return redirect('expediente:expediente_create_oficio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [7,] :
            return redirect('expediente:expediente_create', medio_id=medio_ingreso_id)
        else:
            return redirect('expediente:medio_ingreso_select')


# Paso 2: Formulario de Expediente con MedioIngreso preseleccionado
class DemandaEspontaneaCreateView(LoginRequiredMixin, FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.kwargs.get('medio_id')
        persona_id = self.request.GET.get('persona_id')

        if medio_id:
            initial['medio_ingreso'] = medio_id
            initial['fecha_creacion'] = datetime.date.today
        if persona_id:
            try:
                initial['persona'] = Persona.objects.get(pk=persona_id)
            except Persona.DoesNotExist:
                pass    

        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=ExpedienteDocumento.objects.none()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())
        
        persona_id = self.request.GET.get('persona_id')
        if persona_id:
            context['persona_seleccionada'] = Persona.objects.filter(pk=persona_id).first()    
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            return self.form_invalid(form)

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

        try:
            rol = Rol.objects.get(pk=1)
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol con ID 1 no existe.')
            return self.form_invalid(form)

        expediente = Expediente.objects.create(
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

        ExpedientePersona.objects.create(
            expediente=expediente,
            persona=persona,
            rol=rol
        )

        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        #messages.success(self.request, "Expediente creado con sus documentos.")
        return super().form_valid(form)
    


class DemandaEspontaneaUpdateView(LoginRequiredMixin, FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'

    def get_object(self):
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        expediente = self.get_object()
        initial = super().get_initial()

        # Persona vinculada
        persona_rel = expediente.expedientepersona_expediente.first()
        initial.update({
            'persona': persona_rel.persona if persona_rel else None,
            'sede': expediente.sede,
            'fecha_creacion': expediente.fecha_creacion,
            'medio_ingreso': expediente.medio_ingreso,
            'tipo_solicitud': expediente.tipo_solicitud,
            'estado_expediente': expediente.estado_expediente,
            'grupo_etario': expediente.grupo_etario,
            'edad_persona': expediente.edad_persona,
            'situacion_habitacional_hist': expediente.situacion_habitacional_hist,
            'resumen_intervencion': expediente.resumen_intervencion,
            'observaciones': expediente.observaciones,
        })
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.get_object()

        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                queryset=expediente.documentos.all()
            )

        # Persona seleccionada para mostrar en template
        context['persona_seleccionada'] = (
            expediente.expedientepersona_expediente.first().persona
            if expediente.expedientepersona_expediente.exists()
            else None
        )
         # Indicar que es edición
        context['editar'] = True

        # Número de expediente
        context['numero_expediente'] = expediente.identificador  # ajustar según tu campo real
        return context

    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            return self.form_invalid(form)

        # Actualizar campos del expediente
        expediente.sede = form.cleaned_data['sede']
        expediente.fecha_creacion = form.cleaned_data['fecha_creacion']
        expediente.tipo_solicitud = form.cleaned_data['tipo_solicitud']
        expediente.estado_expediente = form.cleaned_data['estado_expediente']
        expediente.grupo_etario = form.cleaned_data['grupo_etario']
        expediente.edad_persona = form.cleaned_data['edad_persona']
        expediente.situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        expediente.resumen_intervencion = form.cleaned_data['resumen_intervencion']
        expediente.observaciones = form.cleaned_data['observaciones']
        expediente.save()

        # Actualizar o crear relación con persona
        persona = form.cleaned_data['persona']
        rol = Rol.objects.get(pk=1)
        ExpedientePersona.objects.update_or_create(
            expediente=expediente,
            rol=rol,
            defaults={'persona': persona}
        )

        # Guardar documentos
        for documento_form in documento_formset:
            if documento_form.cleaned_data:
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        return super().form_valid(form)



class OficioCreateView(LoginRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.kwargs.get('medio_id')
        institucion_id = self.request.GET.get('institucion_id')
        if medio_id:
            initial['medio_ingreso'] = MedioIngreso.objects.get(pk=medio_id)
            initial['fecha_creacion'] = datetime.date.today()
        if institucion_id:
            initial['institucion'] = institucion_id   
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
        sede = form.cleaned_data['sede']
        fecha_creacion = form.cleaned_data['fecha_creacion']
        medio_ingreso = form.cleaned_data['medio_ingreso']
        fecha_de_juzgado = form.cleaned_data['fecha_de_juzgado']
        fecha_de_recepcion = form.cleaned_data['fecha_de_recepcion']
        expediente_fisico = form.cleaned_data['expediente_fisico']
        cuij = form.cleaned_data['cuij']
        clave_sisfe = form.cleaned_data['clave_sisfe']
        tipo_solicitud = form.cleaned_data['tipo_solicitud']
        estado_expediente = form.cleaned_data['estado_expediente']
        grupo_etario = form.cleaned_data['grupo_etario']
        edad_persona = form.cleaned_data['edad_persona']
        situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        tipo_patrocinio = form.cleaned_data['tipo_patrocinio']
        resumen_intervencion = form.cleaned_data['resumen_intervencion']
        observaciones = form.cleaned_data['observaciones']
        
        try:
            rol = Rol.objects.get(pk=1)
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol no existe.')
            return self.form_invalid(form)

        expediente = Expediente(
            sede = sede,
            fecha_creacion = fecha_creacion,
            medio_ingreso = medio_ingreso,
            fecha_de_juzgado = fecha_de_juzgado,
            fecha_de_recepcion = fecha_de_recepcion,
            expediente_fisico = expediente_fisico,
            cuij = cuij,
            clave_sisfe = clave_sisfe,
            tipo_solicitud = tipo_solicitud,
            estado_expediente = estado_expediente,
            grupo_etario = grupo_etario,
            edad_persona = edad_persona,
            situacion_habitacional_hist = situacion_habitacional_hist,
            tipo_patrocinio = tipo_patrocinio,
            resumen_intervencion = resumen_intervencion,
            observaciones = observaciones,
        )
        expediente.save()  # Identificador generado automáticamente

        try:
            if institucion:
                ExpedienteInstitucion.objects.create(
                    expediente=expediente,
                    institucion=institucion,
                    rol=rol
            )
        except Exception as e:
            messages.error(self.request, f"No se pudo registrar la institución en el expediente: {e}")
            return self.form_invalid(form)
        


class OficioUpdateView(LoginRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'

    # Obtener el expediente a editar
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Expediente, pk=pk)

    def get_initial(self):
        initial = super().get_initial()
        expediente = self.get_object()

        # Si el expediente tiene institución relacionada
        institucion_rel = expediente.expedienteinstitucion_expediente.first()
        if institucion_rel:
            initial.update({
                'institucion': institucion_rel.institucion,
                'sede': getattr(institucion_rel, 'sede', None),
            })

        # Otros campos que vienen directo del expediente
        initial.update({
            'fecha_creacion': expediente.fecha_creacion,
            'medio_ingreso': expediente.medio_ingreso,
            'fecha_de_juzgado': expediente.fecha_de_juzgado,
            'fecha_de_recepcion': expediente.fecha_de_recepcion,
            'expediente_fisico': expediente.expediente_fisico,
            'cuij': expediente.cuij,
            'clave_sisfe': expediente.clave_sisfe,
            'tipo_solicitud': expediente.tipo_solicitud,
            'estado_expediente': expediente.estado_expediente,
            'grupo_etario': expediente.grupo_etario,
            'edad_persona': expediente.edad_persona,
            'situacion_habitacional_hist': expediente.situacion_habitacional_hist,
            'tipo_patrocinio': expediente.tipo_patrocinio,
            'resumen_intervencion': expediente.resumen_intervencion,
            'observaciones': expediente.observaciones,
        })
        return initial
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.get_object()

        # Formset de documentos
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                queryset=expediente.documentos.all()
            )

        # Institución seleccionada
        context['institucion_seleccionada'] = (
            expediente.expedienteinstitucion_expediente.first().institucion
            if expediente.expedienteinstitucion_expediente.exists()
            else None
        )
        
        # Medio de ingreso (usamos el id del medio asociado al expediente)
        context["medio_id"] = expediente.medio_ingreso.id if expediente.medio_ingreso else None  

        context['editar'] = True
        context['numero_expediente'] = expediente.identificador

        return context

    
    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            return self.form_invalid(form)

        # Actualizar los campos del expediente
        for field, value in form.cleaned_data.items():
            setattr(expediente, field, value)
        expediente.save()

        # Actualizar relación con institución
        institucion = form.cleaned_data.get('institucion')
        rol_id = self.request.POST.get('rol_id')  # pasar desde el template
        if institucion and rol_id:
            rol = Rol.objects.get(pk=rol_id)
            ExpedienteInstitucion.objects.update_or_create(
                expediente=expediente,
                rol=rol,
                defaults={'institucion': institucion}
            )

        # Guardar documentos
        for documento_form in documento_formset:
            if documento_form.cleaned_data and not documento_form.cleaned_data.get('DELETE', False):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        return super().form_valid(form) 

        
class SecretariaCreateView(LoginRequiredMixin, FormView):
    template_name = 'expediente/secretaria_form.html'
    form_class = SecretariaForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    

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
        fecha_de_juzgado = form.cleaned_data['fecha_de_juzgado']
        fecha_de_recepcion = form.cleaned_data['fecha_de_recepcion']
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
        
        try:
            rol = Rol.objects.get(pk=1)
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol no existe.')
            return self.form_invalid(form)

        expediente = Expediente(
            fecha_de_juzgado = fecha_de_juzgado,
            fecha_de_recepcion = fecha_de_recepcion,
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


@login_required(login_url = 'core:login')
def expediente_documentos_view(request, expediente_id):
    expediente = get_object_or_404(Expediente, id=expediente_id)

    if request.method == "POST":
        formset = ExpedienteDocumentoFormSet(request.POST, request.FILES, queryset=ExpedienteDocumento.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('archivo'):  # si realmente cargaron un archivo
                    documento = form.save(commit=False)
                    documento.expediente = expediente
                    documento.save()
            messages.success(request, "Documentos cargados correctamente.")
            return redirect("expediente:expediente_detail", pk=expediente.id)
    else:
        formset = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())

    return render(request, "expediente/expediente_documentos_form.html", {
        "formset": formset,
        "expediente": expediente,
    })



