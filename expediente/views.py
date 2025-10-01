# Importamos algunas librerías necesarias para trabajar con fechas y vistas en Django
import datetime
from django.views.generic import FormView
from django.urls import reverse_lazy

# Mezclas para controlar permisos y autenticación de usuarios
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

# Vistas genéricas para mostrar listas y editar objetos
from django.views.generic import ListView, UpdateView

# Funciones para redirigir usuarios y obtener objetos de la base de datos
from django.shortcuts import redirect

# Importamos los formularios que se usarán en las vistas
from .forms import DemandaEspontanea, MedioIngresoForm, OficioForm, SecretariaForm

# Importamos los modelos (tablas) que usaremos para guardar y consultar información
from .models import Expediente, ExpedientePersona, Rol, ExpedienteInstitucion, ExpedienteDocumento, MedioIngreso
from persona.models import Persona
from institucion.models import Institucion

# Funciones para renderizar páginas y mostrar mensajes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ExpedienteDocumentoFormSet
from django.views import View


# Vista para listar todos los expedientes (casos)
class ExpedienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Expediente  # Usamos el modelo Expediente
    template_name = 'expediente/expediente_list.html'  # HTML que se usará para mostrar la lista
    context_object_name = 'expedientes'  # Nombre de la variable que contiene los expedientes en el HTML
    login_url = 'core:login'  # Si el usuario no está logueado, lo enviamos a esta página
    permission_required = 'expediente.view_expediente' # Permiso necesario para ver expedientes
    raise_exception = True  # Si no tiene permiso, muestra error 403

    def get_queryset(self):
        # Retorna todos los expedientes ordenados por identificador
        return Expediente.objects.all().order_by('-identificador')

# Vista para seleccionar el medio de ingreso, primer paso para crear un expediente
class MedioIngresoSelectView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/medio_ingreso.html'
    form_class = MedioIngresoForm
    login_url = 'core:login'
    permission_required = 'expediente.view_medioingreso'
    raise_exception = True
    
    def get_initial(self):
        initial = super().get_initial()
        # Busca el medio "Demanda Espontánea"
        medio = MedioIngreso.objects.filter().first()
        if medio:
            initial['medio_ingreso'] = medio
        return initial

 
    def form_valid(self, form):
        # Esta función decide a qué formulario redirigir según el medio de ingreso elegido
        medio_ingreso_id = form.cleaned_data['medio_ingreso'].id

        if medio_ingreso_id in [1,] :
            # Si el medio es 1, redirige a crear expediente con ese medio
            return redirect('expediente:expediente_create_with_medio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [2, 3, 4, 5, 6] :
            # Si el medio es entre 2 y 6, redirige a crear expediente tipo oficio
            return redirect('expediente:expediente_create_oficio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [7,] :
            # Si el medio es 7, redirige a crear expediente normal
            return redirect('expediente:expediente_create', medio_id=medio_ingreso_id)
        else:
            # Si no coincide, vuelve a la selección
            return redirect('expediente:medio_ingreso_select')

# Vista que decide qué formulario mostrar para editar según el tipo de expediente
class ExpedienteUpdateDispatcherView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = True

    def get(self, request, pk):
        expediente = get_object_or_404(Expediente, pk=pk)
        medio = expediente.medio_ingreso.medio_ingreso if expediente.medio_ingreso else ""

        # Según el medio de ingreso, redirige al formulario correcto
        # Para editar cada tipo de expediente usamos las vistas ya definidas y registradas en urls.py
        # Cada tipo de expediente tiene su propia vista de edición

        medios_oficio = [
            "OFICIO POR MAIL",
            "OFICIO PAPEL",
            "DERIVACION",
            "MAIL EFECTOR",
            "COMUNICACION TELEFONICA EQUIPO TRATANTE",
        ]

        if medio == "DEMANDA ESPONTANEA":
            return redirect('expediente:demanda_espontanea_update', pk=pk)
        elif medio in medios_oficio:
            return redirect('expediente:oficio_update', pk=pk)
        elif medio == "SOLICITUD SECRETARIA EJECUTIVA (DE OFICIO)":
            return redirect('expediente:secretaria_update', pk=pk)
        else:
            # Si no reconoce el medio, muestra error
            messages.error(request, "No se pudo determinar el tipo de expediente.")
            return redirect('expediente:expediente_list')


# Vista para crear expedientes del tipo "Demanda Espontanea"
# Es el expediente más común y tiene a la persona como actor principal
class DemandaEspontaneaCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expediente'
    raise_exception = True

    def get_initial(self):
        # Prepara los datos iniciales del formulario, como el medio de ingreso y la fecha
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
        # Crea el formulario y deshabilita el campo medio_ingreso
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        # Prepara datos adicionales para la plantilla, como el formset de documentos
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
        # Si el formulario es válido, crea el expediente y las relaciones necesarias
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
            
        # Extrae datos del formulario
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

        # Crea el expediente
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

        # Relaciona la persona con el expediente
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

        # Guarda los documentos vinculados al expediente
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue creado correctamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Muestra mensaje si hubo errores
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)


# (Las siguientes vistas siguen la misma lógica: muestran formularios, validan datos, crean o actualizan objetos en la base de datos, y preparan datos para mostrar en el HTML. Cada clase tiene comentarios en las partes principales del flujo.)
class DemandaEspontaneaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso

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



class OficioCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expediente'
    raise_exception = True

    def get_medio_id(self):
        """Obtiene medio_id desde kwargs o GET, priorizando kwargs."""
        return self.kwargs.get('medio_id') or self.request.GET.get('medio_id')

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.get_medio_id()
        institucion_id = self.request.GET.get('institucion_id')

        # Set medio_ingreso from URL/GET only once (not in POST)
        if medio_id:
            medio = get_object_or_404(MedioIngreso, pk=medio_id)
            initial['medio_ingreso'] = medio
            initial['fecha_creacion'] = datetime.date.today()

        if institucion_id:
            try:
                initial['institucion'] = Institucion.objects.get(pk=institucion_id)
            except Institucion.DoesNotExist:
                pass

        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        # Campo de medio_ingreso: solo lectura visual, pero editable internamente.
        form.fields['medio_ingreso'].disabled = True
        form.fields['medio_ingreso'].widget.attrs['style'] = 'pointer-events: none; background-color: #f8f9fa;'  # Estilo visual
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=ExpedienteDocumento.objects.none()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())

        institucion_id = self.request.GET.get('institucion_id')
        if institucion_id:
            context['institucion_seleccionada'] = Institucion.objects.filter(pk=institucion_id).first()

        # --- FIX: añade medio_id al contexto ---
        context['medio_id'] = self.get_medio_id()
        # ---------------------------------------
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
            return self.form_invalid(form)

        institucion = form.cleaned_data.get('institucion')
        if not institucion:
            form.add_error('institucion', 'Debe seleccionar una institución')
            messages.error(self.request, "Debe seleccionar una institución para crear el expediente.")
            return self.form_invalid(form)

        # Obtiene el medio_ingreso SIEMPRE desde la URL o GET, no del form.cleaned_data 
        medio_id = self.get_medio_id()
        medio_ingreso = get_object_or_404(MedioIngreso, pk=medio_id)

        # Obtiene el resto normalmente
        sede = form.cleaned_data.get('sede')
        fecha_creacion = form.cleaned_data.get('fecha_creacion')
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

        try:
            rol = Rol.objects.get(pk=2)
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol predeterminado no existe.')
            return self.form_invalid(form)

        # Crea el expediente con el medio_ingreso correcto
        expediente = Expediente.objects.create(
            sede=sede,
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,  # <-- SIEMPRE desde URL o GET
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

        # Relación con institución
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

        # Vincula documentos
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
    
    

class OficioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso

    def get_object(self):
        # Obtiene el expediente por la pk de la URL
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        # Carga los datos existentes del expediente en el formulario
        expediente = self.get_object()
        initial = super().get_initial()
        institucion_rel = expediente.expedienteinstitucion_expediente.first()

        initial.update({
            'institucion': institucion_rel.institucion if institucion_rel else None,
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
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=expediente.documentos.all())

        institucion_rel = expediente.expedienteinstitucion_expediente.first()
        context['institucion_seleccionada'] = institucion_rel.institucion if institucion_rel else None
        return context

    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
            return self.form_invalid(form)

        institucion = form.cleaned_data.get('institucion')
        if not institucion:
            form.add_error('institucion', 'Debe seleccionar una institución')
            messages.error(self.request, "Debe seleccionar una institución para actualizar el expediente.")
            return self.form_invalid(form)

        # Actualiza los datos del expediente
        expediente.sede = form.cleaned_data.get('sede')
        expediente.fecha_creacion = form.cleaned_data.get('fecha_creacion')
        expediente.medio_ingreso = form.cleaned_data.get('medio_ingreso')
        expediente.fecha_de_juzgado = form.cleaned_data.get('fecha_de_juzgado')
        expediente.fecha_de_recepcion = form.cleaned_data.get('fecha_de_recepcion')
        expediente.expediente_fisico = form.cleaned_data.get('expediente_fisico')
        expediente.cuij = form.cleaned_data.get('cuij')
        expediente.clave_sisfe = form.cleaned_data.get('clave_sisfe')
        expediente.tipo_solicitud = form.cleaned_data.get('tipo_solicitud')
        expediente.estado_expediente = form.cleaned_data.get('estado_expediente')
        expediente.grupo_etario = form.cleaned_data.get('grupo_etario')
        expediente.edad_persona = form.cleaned_data.get('edad_persona')
        expediente.situacion_habitacional_hist = form.cleaned_data.get('situacion_habitacional_hist')
        expediente.tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        expediente.resumen_intervencion = form.cleaned_data.get('resumen_intervencion')
        expediente.observaciones = form.cleaned_data.get('observaciones')
        expediente.save()

        # Actualiza o crea relación con institución
        try:
            rol = Rol.objects.get(pk=2)
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol predeterminado no existe.')
            return self.form_invalid(form)

        ExpedienteInstitucion.objects.update_or_create(
            expediente=expediente,
            rol=rol,
            defaults={'institucion': institucion}
        )

        # Actualiza documentos vinculados al expediente
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue actualizado correctamente.")
        return super().form_valid(form)   

    def form_invalid(self, form):
        messages.error(self.request, "Hubo errores al actualizar el expediente. Verifique los campos.")
        return super().form_invalid(form)

# class OficioUpdateView_(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     # Establece el HTML que se usará para mostrar el formulario de edición
#     template_name = 'expediente/oficio_form.html'
#     # Indica qué formulario se usará para editar los datos
#     form_class = OficioForm
#     # Modelo que se va a modificar (la tabla Expediente)
#     model = Expediente
#     # URL a la que se redirige cuando todo sale bien
#     success_url = reverse_lazy('expediente:expediente_list')
#     # Si el usuario no está logueado, lo envía al login
#     login_url = 'core:login'
#     # Permiso necesario para poder editar un expediente
#     permission_required = 'expediente.change_expediente'
#     # Si el usuario no tiene permiso, muestra un error 403 (prohibido)
#     raise_exception = True

#     def get_form(self, form_class=None):
#         # Esta función se encarga de crear el formulario que verá el usuario
#         form = super().get_form(form_class)  # Llama al método original para crear el form
#         form.fields['medio_ingreso'].disabled = True  # Desactiva el campo medio_ingreso para que no se pueda modificar
#         return form

#     def get_context_data(self, **kwargs):
#         # Agrega información extra para el template HTML
#         context = super().get_context_data(**kwargs)
#         expediente = self.object  # El expediente que se está editando

#         # Si el usuario envió datos por POST (está guardando el formulario)
#         if self.request.POST:
#             # Crea el formset (grupo de formularios) para los documentos enviados
#             context['documento_formset'] = ExpedienteDocumentoFormSet(
#                 self.request.POST, self.request.FILES,
#                 queryset=expediente.documentos.all()
#             )
#         else:
#             # Si está entrando por GET (solo viendo el formulario), muestra los documentos ya guardados
#             context['documento_formset'] = ExpedienteDocumentoFormSet(
#                 queryset=expediente.documentos.all()
#             )

#         # Busca la institución vinculada al expediente (si existe)
#         context['institucion_seleccionada'] = (
#             expediente.expedienteinstitucion_expediente.first().institucion
#             if expediente.expedienteinstitucion_expediente.exists()
#             else None
#         )
#         # Le dice al template que está en modo edición
#         context['editar'] = True
#         # Pasa el número de expediente para mostrarlo en el formulario
#         context['numero_expediente'] = expediente.identificador
#         return context

#     def form_valid(self, form):
#         # Esta función se ejecuta si el formulario principal es válido
#         expediente = form.save(commit=False)  # Guarda los datos pero aún no en la base de datos

#         context = self.get_context_data()
#         documento_formset = context['documento_formset']

#         # Verifica que el formset de documentos también sea válido
#         if not documento_formset.is_valid():
#             return self.form_invalid(form)

#         expediente.save()  # Guarda los cambios del expediente en la base de datos

#         # Guarda la institución que se relaciona con el expediente
#         institucion = form.cleaned_data['institucion']
#         rol = Rol.objects.get(pk=1)  # Obtiene el rol por defecto (puedes cambiar el ID según tu sistema)
#         ExpedienteInstitucion.objects.update_or_create(
#             expediente=expediente,
#             rol=rol,
#             defaults={'institucion': institucion}
#         )

#         # Guarda cada documento subido por el usuario, relacionándolos con el expediente
#         documentos = documento_formset.save(commit=False)
#         for doc in documentos:
#             doc.expediente = expediente  # Relaciona el documento con el expediente
#             doc.save()  # Guarda el documento en la base de datos

#         return super().form_valid(form)  # Redirige al success_url



class SecretariaCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/secretaria_form.html'
    form_class = SecretariaForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expediente'
    raise_exception = True  # devuelve 403 Forbidden si no tiene permiso

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.kwargs.get('medio_id')
        
        # Medio de ingreso
        if medio_id:
            medio = get_object_or_404(MedioIngreso, pk=medio_id)
            initial['medio_ingreso'] = medio
            initial['fecha_creacion'] = datetime.date.today()

        return initial

    #Función del formulario para obtener usuario y medio de ingreso
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form
    
    def get_context_data(self, **kwargs):
        # Prepara datos adicionales para la plantilla, como el formset de documentos
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=ExpedienteDocumento.objects.none()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())
        
                  
        return context

    def form_valid(self, form):
        # Si el formulario es válido, crea el expediente y las relaciones necesarias
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
            return self.form_invalid(form)

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
        tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        expediente_fisico = form.cleaned_data['expediente_fisico']
        clave_sisfe = form.cleaned_data['clave_sisfe']
        cuij = form.cleaned_data['cuij']
        observaciones = form.cleaned_data['observaciones']
        
        
        
        
        try:
            rol = Rol.objects.get(pk=3)  # Asumimos que el rol con ID 3 es "Solicitante"
        except Rol.DoesNotExist:
            form.add_error(None, 'El rol no existe.')
            return self.form_invalid(form)

        expediente = Expediente.objects.create(
            fecha_de_juzgado=fecha_de_juzgado,
            fecha_de_recepcion=fecha_de_recepcion,
            sede=sede,
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,
            tipo_solicitud = tipo_solicitud,
            estado_expediente = estado_expediente,
            grupo_etario = grupo_etario,
            edad_persona = edad_persona,
            situacion_habitacional_hist = situacion_habitacional_hist,
            resumen_intervencion = resumen_intervencion,
            tipo_patrocinio = tipo_patrocinio,
            expediente_fisico = expediente_fisico,
            clave_sisfe = clave_sisfe,
            cuij = cuij,
            observaciones = observaciones,

        )
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue creado correctamente.")
        return super().form_valid(form)
        

    def form_invalid(self, form):
        # Muestra mensaje si hubo errores
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error en {field.label}: {error}")
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)



class SecretariaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/secretaria_form.html'
    form_class = SecretariaForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = True

    def get_object(self):
        # Obtiene el expediente por la pk de la URL
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        # Carga los datos existentes del expediente en el formulario
        expediente = self.get_object()
        initial = super().get_initial()
        initial.update({
            'fecha_de_juzgado': expediente.fecha_de_juzgado,
            'fecha_de_recepcion': expediente.fecha_de_recepcion,
            'sede': expediente.sede,
            'fecha_creacion': expediente.fecha_creacion,
            'medio_ingreso': expediente.medio_ingreso,
            'tipo_solicitud': expediente.tipo_solicitud,
            'estado_expediente': expediente.estado_expediente,
            'grupo_etario': expediente.grupo_etario,
            'edad_persona': expediente.edad_persona,
            'situacion_habitacional_hist': expediente.situacion_habitacional_hist,
            'resumen_intervencion': expediente.resumen_intervencion,
            'tipo_patrocinio': expediente.tipo_patrocinio,
            'expediente_fisico': expediente.expediente_fisico,
            'clave_sisfe': expediente.clave_sisfe,
            'cuij': expediente.cuij,
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
                self.request.POST, self.request.FILES, queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=expediente.documentos.all())
        return context

    def form_valid(self, form):
        # Actualiza el expediente con los nuevos datos
        expediente = self.get_object()
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        if not documento_formset.is_valid():
            messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
            return self.form_invalid(form)

        expediente.fecha_de_juzgado = form.cleaned_data['fecha_de_juzgado']
        expediente.fecha_de_recepcion = form.cleaned_data['fecha_de_recepcion']
        expediente.sede = form.cleaned_data['sede']
        expediente.fecha_creacion = form.cleaned_data['fecha_creacion']
        expediente.medio_ingreso = form.cleaned_data['medio_ingreso']
        expediente.tipo_solicitud = form.cleaned_data['tipo_solicitud']
        expediente.estado_expediente = form.cleaned_data['estado_expediente']
        expediente.grupo_etario = form.cleaned_data['grupo_etario']
        expediente.edad_persona = form.cleaned_data['edad_persona']
        expediente.situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        expediente.resumen_intervencion = form.cleaned_data['resumen_intervencion']
        expediente.tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        expediente.expediente_fisico = form.cleaned_data['expediente_fisico']
        expediente.clave_sisfe = form.cleaned_data['clave_sisfe']
        expediente.cuij = form.cleaned_data['cuij']
        expediente.observaciones = form.cleaned_data['observaciones']
        expediente.save()

        # Actualiza o crea los documentos asociados
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Muestra mensaje si hubo errores, incluyendo los de cada campo
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error en {field.label}: {error}")
        messages.error(self.request, "Hubo errores al actualizar el expediente. Verifique los campos.")
        return super().form_invalid(form)        





# Vista basada en función para subir documentos de un expediente
@login_required(login_url = 'core:login')
@permission_required('expediente.add_expedientedocumento', login_url='core:login', raise_exception=True)
def expediente_documentos_view(request, expediente_id):
    # Obtiene el expediente por ID
    expediente = get_object_or_404(Expediente, id=expediente_id)

    if request.method == "POST":
        # Si el usuario envió archivos, procesa el formset
        formset = ExpedienteDocumentoFormSet(request.POST, request.FILES, queryset=ExpedienteDocumento.objects.none())
        if formset.is_valid():
            # Guarda cada documento subido
            for form in formset:
                if form.cleaned_data.get('archivo'):  # si realmente cargaron un archivo
                    documento = form.save(commit=False)
                    documento.expediente = expediente
                    documento.save()
            messages.success(request, "Documentos cargados correctamente.")
            return redirect("expediente:expediente_detail", pk=expediente.id)
    else:
        # Si es GET, muestra el formulario vacío
        formset = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())

    # Renderiza el formulario HTML con los documentos y expediente
    return render(request, "expediente/expediente_documentos_form.html", {
        "formset": formset,
        "expediente": expediente,
    })
    
    
def expediente_list(request):
    expedientes = Expediente.objects.all()
    next_url = request.GET.get("next")       # para redirigir después

    return render(request, "expediente/expediente_buscar.html", {
        "expedientes": expedientes,
        "next_url": next_url,   # lo mandamos al template
    })
