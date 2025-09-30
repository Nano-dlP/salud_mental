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
