from django import forms

from .models import Expediente
from institucion.models import Institucion

class ExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expediente
        fields = [
            'localidad', 'fecha_de_juzgado', 'fecha_de_recepcion', 'expediente_fisico', 'cuij',
            'clave_sisfe', 'medio_ingreso', 'situacion_habitacional_hist', 'tipo_solicitud',
            'grupo_etario', 'tipo_patrocinio', 'resumen_intervencion', 'estado_expediente'            
        ]

        widgets = {
            'localidad':forms.Select(attrs={'class': 'form-control'}),
            'fecha_de_juzgado': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'fecha_de_recepcion': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'expediente_fisico': forms.CheckboxInput(attrs={'class': 'form-check-input form-check-input-sm'}),
            'cuij': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Clave Única de Identificación Judicial'}),
            'clave_sisfe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese clave SISFE'}),
            'medio_ingreso':forms.Select(attrs={'class': 'form-control'}),
            'situacion_habitacional_hist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese situación habitacional histórica'}),
            'tipo_solicitud':forms.Select(attrs={'class': 'form-control'}),
            'grupo_etario':forms.Select(attrs={'class': 'form-control'}),
            'tipo_patrocinio':forms.Select(attrs={'class': 'form-control'}),
            'estado_expediente':forms.Select(attrs={'class': 'form-control'}),
            'resumen_intervencion':forms.Select(attrs={'class': 'form-control'}),

        }





