# views.py
import datetime
from django.views.generic import FormView
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.shortcuts import redirect
from .forms import DemandaEspontanea, MedioIngresoForm, OficioForm, SecretariaForm
from .models import Expediente, ExpedientePersona, Rol, ExpedienteInstitucion, ExpedienteDocumento, MedioIngreso
from persona.models import Persona

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ExpedienteDocumentoFormSet
from django.views import View



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


class ExpedienteUpdateDispatcherView(LoginRequiredMixin, View):
    login_url = 'core:login'

    def get(self, request, pk):
        expediente = get_object_or_404(Expediente, pk=pk)
        medio = expediente.medio_ingreso.medio_ingreso if expediente.medio_ingreso else ""

        # Redirigir a la vista correspondiente según medio de ingreso
        if medio == "DEMANDA ESPONTANEA":
            return redirect('expediente:demanda_espontanea_update', pk=pk)
        elif medio == "OFICIO POR MAIL":
            return redirect('expediente:oficio_update', pk=pk)
        elif medio == "Secretaria":
            return redirect('expediente:secretaria_update', pk=pk)
        else:
            messages.error(request, "No se pudo determinar el tipo de expediente.")
            return redirect('expediente:expediente_list')



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
            messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
            return self.form_invalid(form)

        persona = form.cleaned_data.get('persona')
        if not persona:
            form.add_error('persona', 'Debe seleccionar una persona')
            messages.error(self.request, "Debe seleccionar una persona para crear el expediente.")
            return self.form_invalid(form)
            
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

        # Retornar HttpResponse correcto
        if persona:
            try:
                ExpedientePersona.objects.create(
                    expediente=expediente,
                    persona=persona,
                    rol=rol
                )
            except Exception as e:
                messages.error(self.request, f"No se pudo registrar la persona: {e}")
                return self.form_invalid(form)

        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue creado correctamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)
        


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

        # Medio de ingreso
        if medio_id:
            medio = get_object_or_404(MedioIngreso, pk=medio_id)
            initial['medio_ingreso'] = medio
            initial['fecha_creacion'] = datetime.date.today()

        # Institución opcional (solo si viene por GET)
        if institucion_id:
            from .models import Institucion
            institucion = get_object_or_404(Institucion, pk=institucion_id)
            initial['institucion'] = institucion

        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        # Deshabilitar campo de medio_ingreso para que no se modifique
        form.fields['medio_ingreso'].disabled = True
        return form

    def form_valid(self, form):
        # Obtener datos del formulario
        institucion = form.cleaned_data.get('institucion')
        sede = form.cleaned_data.get('sede')
        fecha_creacion = form.cleaned_data.get('fecha_creacion')
        medio_ingreso = form.cleaned_data.get('medio_ingreso')
        fecha_de_juzgado = form.cleaned_data.get('fecha_de_juzgado')
        fecha_de_recepcion = form.cleaned_data.get('fecha_de_recepcion')
        expediente_fisico = form.cleaned_data.get('expediente_fisico')
        cuij = form.cleaned_data.get('cuij')
        clave_sisfe = form.cleaned_data.get('clave_sisfe')
        tipo_solicitud = form.cleaned_data.get('tipo_solicitud')
        estado_expediente = form.cleaned_data.get('estado_expediente')
        grupo_etario = form.cleaned_data.get('grupo_etario')
        edad_persona = form.cleaned_data.get('edad_persona')
        situacion_habitacional_hist = form.cleaned_data.get('situacion_habitacional_hist')
        tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        resumen_intervencion = form.cleaned_data.get('resumen_intervencion')
        observaciones = form.cleaned_data.get('observaciones')

        # Obtener rol predeterminado
        try:
            rol = Rol.objects.get(pk=1)
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol predeterminado no existe.')
            return self.form_invalid(form)

        # Crear expediente sin pasar institucion (se guarda en relación aparte)
        expediente = Expediente(
            sede=sede,
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,
            fecha_de_juzgado=fecha_de_juzgado,
            fecha_de_recepcion=fecha_de_recepcion,
            expediente_fisico=expediente_fisico,
            cuij=cuij,
            clave_sisfe=clave_sisfe,
            tipo_solicitud=tipo_solicitud,
            estado_expediente=estado_expediente,
            grupo_etario=grupo_etario,
            edad_persona=edad_persona,
            situacion_habitacional_hist=situacion_habitacional_hist,
            tipo_patrocinio=tipo_patrocinio,
            resumen_intervencion=resumen_intervencion,
            observaciones=observaciones
        )
        expediente.save()

        # Guardar relación con institución (si existe)
        if institucion:
            try:
                ExpedienteInstitucion.objects.create(
                    expediente=expediente,
                    institucion=institucion,
                    rol=rol
                )
            except Exception as e:
                messages.error(self.request, f"No se pudo registrar la institución: {e}")
                return self.form_invalid(form)

        # Retornar HttpResponse correcto
        return super().form_valid(form)        



class OficioUpdateView(LoginRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        initial = super().get_initial()
        expediente = self.get_object()

        #Institución vinculada al expediente
        institucion_rel = expediente.expedienteinstitucion_expediente.first()
        if institucion_rel:
            initial['institucion'] = institucion_rel.institucion
            initial['sede'] = getattr(institucion_rel, 'sede', None)
        
        # Otros campos del expediente
        initial.update({
            'fecha_creacion': expediente.fecha_creacion,
            'sede': expediente.sede,
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
        context['documento_formset'] = ExpedienteDocumentoFormSet(
            self.request.POST or None,
            self.request.FILES or None,
            queryset=expediente.documentos.all()
        )
        context['institucion_seleccionada'] = (
            expediente.expedienteinstitucion_expediente.first().institucion
            if expediente.expedienteinstitucion_expediente.exists() else None
        )
        context['medio_id'] = expediente.medio_ingreso.id if expediente.medio_ingreso else None
        context['editar'] = True
        context['numero_expediente'] = expediente.identificador
        return context

    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        documento_formset = context.get('documento_formset')

        # Validar formset
        if documento_formset and not documento_formset.is_valid():
            return self.form_invalid(form)

        # Actualizar campos del expediente manualmente
        for field, value in form.cleaned_data.items():
            if field != 'institucion':  # Institución se guarda en la relación
                setattr(expediente, field, value)
        expediente.save()

        # Actualizar relación con institución
        institucion = form.cleaned_data.get('institucion')
        rol_id = self.request.POST.get('rol_id')  # Debe venir del template
        if institucion and rol_id:
            try:
                rol = Rol.objects.get(pk=rol_id)
                ExpedienteInstitucion.objects.update_or_create(
                    expediente=expediente,
                    rol=rol,
                    defaults={'institucion': institucion}
                )
            except Rol.DoesNotExist:
                messages.error(self.request, 'El rol seleccionado no existe.')
                return self.form_invalid(form)

        # Guardar documentos
        if documento_formset:
            for doc_form in documento_formset:
                if doc_form.cleaned_data and not doc_form.cleaned_data.get('DELETE', False):
                    documento = doc_form.save(commit=False)
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

