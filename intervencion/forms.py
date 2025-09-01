from django import forms
from .models import Intervencion, TipoIntervencion
from expediente.models import Expediente
from profesional.models import Profesional

class IntervencionForm(forms.Form):
    expediente = forms.ModelChoiceField(queryset=Expediente.objects.all(), label="Expediente")
    profesional = forms.ModelChoiceField(queryset=Profesional.objects.all(), label="Profesional")
    tipo_intervencion = forms.ModelChoiceField(queryset=TipoIntervencion.objects.all(), label="Tipo de intervención")
    fecha_intervencion = forms.DateTimeField(label="Fecha de intervención", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    observacion = forms.CharField(label="Observaciones", widget=forms.Textarea, required=False)

    def save(self):
        data = self.cleaned_data
        intervencion = Intervencion(
            expediente=data['expediente'],
            profesional=data['profesional'],
            tipo_intervencion=data['tipo_intervencion'],
            fecha_intervencion=data['fecha_intervencion'],
            observacion=data['observacion']
        )
        intervencion.save()
        return intervencion