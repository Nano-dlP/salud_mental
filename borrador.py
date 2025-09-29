
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
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)



