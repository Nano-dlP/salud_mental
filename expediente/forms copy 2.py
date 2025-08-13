import datetime
from django import forms
from core.models import Rol
from persona.models import Persona
from .models import Expediente, MedioIngreso, TipoSolicitud, GrupoEtario, ResumenIntervencion, TipoPatrocinio, EstadoExpediente
from core.models import Sede


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


class DemandaEspontanea(forms.Form):
    fecha_de_creacion = forms.DateField(
        initial=datetime.date.today, 
        widget=forms.DateInput(
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
                'readonly': 'readonly'
            }
        )
    )
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    medio_ingreso = forms.ModelChoiceField(
        queryset=MedioIngreso.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_solicitud = forms.ModelChoiceField(
        queryset=TipoSolicitud.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    estado_expediente = forms.ModelChoiceField(
        queryset=EstadoExpediente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grupo_etario = forms.ModelChoiceField(
        queryset=GrupoEtario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    edad_persona = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    situacion_habitacional_hist = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    resumen_intervencion = forms.ModelChoiceField(
        queryset=ResumenIntervencion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )