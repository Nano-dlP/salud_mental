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

        # Institución vinculada
        institucion_rel = expediente.expedienteinstitucion_expediente.first()

        # El rol viene de la relación institucion_rel
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
            'rol': institucion_rel.rol if institucion_rel else None,
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
                self.request.POST,
                self.request.FILES,
                queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                queryset=expediente.documentos.all()
            )

        # Institución seleccionada para mostrar en template
        institucion_rel = expediente.expedienteinstitucion_expediente.first()
        context['institucion_seleccionada'] = institucion_rel.institucion if institucion_rel else None
        context['rol_seleccionado'] = institucion_rel.rol if institucion_rel else None

        # Indicar que es edición
        context['editar'] = True

        # Número de expediente
        context['numero_expediente'] = expediente.identificador  # ajustar según tu campo real
        return context

    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        #documento_formset = context['documento_formset']

        #if not documento_formset.is_valid():
        #    messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
        #    return self.form_invalid(form)

        institucion_obj = form.cleaned_data.get('institucion')
        
        if not institucion_obj:
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

        # Actualiza o crea relación con institución (versión robusta)
        rol = form.cleaned_data.get('rol')

        # Buscar relación exacta por expediente + institución
        exact_qs = ExpedienteInstitucion.objects.filter(
            expediente=expediente, institucion=institucion_obj
        )

        if exact_qs.exists():
            # Tomamos la primera relación encontrada y actualizamos el rol si cambió
            ei_obj = exact_qs.order_by('id').first()
            if ei_obj.rol != rol:
                ei_obj.rol = rol
                ei_obj.save()
                logger.info(
                    "Actualizado rol de ExpedienteInstitucion id=%s a rol=%s (expediente=%s, institucion=%s)",
                    ei_obj.pk, rol, expediente.pk, getattr(institucion_obj, 'pk', institucion_obj)
                )

            # Si hay duplicados exactos (mismas institucion+expediente), los dejamos registrados para limpieza
            duplicates = exact_qs.exclude(pk=ei_obj.pk)
            if duplicates.exists():
                logger.warning(
                    "Se encontraron %d ExpedienteInstitucion duplicadas para expediente=%s institucion=%s. "
                    "Manteniendo id=%s. Considerar limpiar la DB.",
                    duplicates.count(), expediente.pk, getattr(institucion_obj, 'pk', institucion_obj), ei_obj.pk
                )
                # Opcional: eliminar duplicados automáticamente (descomentar si quieres borrar)
                # duplicates.delete()
        else:
            # No existe relación exacta -> crear nueva relación con el rol seleccionado
            ExpedienteInstitucion.objects.create(expediente=expediente, institucion=institucion_obj, rol=rol)
            logger.info(
                "Creada nueva ExpedienteInstitucion expediente=%s institucion=%s rol=%s",
                expediente.pk, getattr(institucion_obj, 'pk', institucion_obj), rol
            )

        # Actualiza documentos vinculados al expediente (si vuelves a activarlos)
        # for documento_form in documento_formset:
        #     if documento_form.cleaned_data.get('archivo'):
        #         documento = documento_form.save(commit=False)
        #         documento.expediente = expediente
        #         documento.save()

        messages.success(self.request, "El expediente fue actualizado correctamente.")
        return super().form_valid(form)

    