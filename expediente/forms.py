from django import forms
from core.models import Rol
from persona.models import Persona
from .models import Expediente, MedioIngreso, ExpedientePersona


class MedioIngresoForm(forms.Form):
    medio_ingreso = forms.ModelChoiceField(
        queryset=MedioIngreso.objects.all(),
        label="Medio de Ingreso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ExpedienteCompletoForm(forms.ModelForm):
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        label="Persona",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label="Rol",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Expediente
        fields = [
            'sede', 'tipo_solicitud', 'grupo_etario', 'tipo_patrocinio',
            'edad_persona', 'situacion_habitacional', 'resumen_intervencion', 'observaciones'
        ]
        widgets = {
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'tipo_solicitud': forms.Select(attrs={'class': 'form-control'}),
            'grupo_etario': forms.Select(attrs={'class': 'form-control'}),
            'tipo_patrocinio': forms.Select(attrs={'class': 'form-control'}),
            'edad_persona': forms.NumberInput(attrs={'class': 'form-control'}),
            'situacion_habitacional': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen_intervencion': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }
