import datetime
from django.shortcuts import render
from django import forms
from core.models import Rol
from persona.models import Persona
from institucion.models import Institucion
from .models import Expediente, MedioIngreso, TipoSolicitud, GrupoEtario, ResumenIntervencion, TipoPatrocinio, EstadoExpediente
from core.models import Sede
from django.conf import settings



#usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)



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
            'edad_persona', 'situacion_habitacional_hist', 'resumen_intervencion', 'observaciones'
        ]
        widgets = {
            'sede': forms.Select(attrs={'class': 'form-control'}),
            #'fecha_creacion': forms.Select(attrs={'class': 'form-control'}),
            'tipo_solicitud': forms.Select(attrs={'class': 'form-control'}),
            'grupo_etario': forms.Select(attrs={'class': 'form-control'}),
            'tipo_patrocinio': forms.Select(attrs={'class': 'form-control'}),
            'edad_persona': forms.NumberInput(attrs={'class': 'form-control'}),
            'situacion_habitacional_hist': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen_intervencion': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }


class DemandaEspontanea(forms.Form):
    fecha_creacion = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
                'readonly': 'readonly'
            }
        ),
        input_formats=['%Y-%m-%d']
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
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    resumen_intervencion = forms.ModelChoiceField(
        queryset=ResumenIntervencion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    
    #Con esta función obtenemos la sede asignada al usuario para cargar el formulario
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtenemos el usuario desde la vista
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated and hasattr(user, 'sede'):
            self.fields['sede'].initial = user.sede  # Valor inicial
            self.fields['sede'].queryset = Sede.objects.filter(id=user.sede.id)  # Solo su sede
            self.fields['sede'].disabled = True  # Opcional: para que no pueda cambiarla
            
            
class OficioForm(forms.Form):
    fecha_creacion = forms.DateField(
        label="Fecha de creación:",
        initial=datetime.date.today,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
                'readonly': 'readonly'
            }
        ),
        input_formats=['%Y-%m-%d']
    )
    institucion = forms.ModelChoiceField(
        label="Institución:",
        queryset=Institucion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_de_juzgado = forms.DateField(
        label="Fecha de ingreso al juzgado:",
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
                }
        ),
        input_formats=['%Y-%m-%d']
    )
    
    fecha_de_recepcion = forms.DateField(
        label="Fecha de recepción del oficio",
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
                }
        ),
        input_formats=['%Y-%m-%d']
    )
    
    persona = forms.ModelChoiceField(
        label="Persona",
        queryset=Persona.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sede = forms.ModelChoiceField(
        label="Sede",
        queryset=Sede.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    medio_ingreso = forms.ModelChoiceField(
        label="Medio de ingreso:",
        queryset=MedioIngreso.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_solicitud = forms.ModelChoiceField(
        label="Tipo de solicitud:",
        queryset=TipoSolicitud.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    estado_expediente = forms.ModelChoiceField(
        label="Estado del expediente:",
        queryset=EstadoExpediente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grupo_etario = forms.ModelChoiceField(
        label="Grupo Etario al que pertenece:",
        queryset=GrupoEtario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    edad_persona = forms.IntegerField(
        label="Edad de la persona:",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    situacion_habitacional_hist = forms.CharField(
        label="Situación habitacional histórica:",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    resumen_intervencion = forms.ModelChoiceField(
        label="Resumén de intervención:",
        queryset=ResumenIntervencion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    expediente_fisico = forms.BooleanField(
        required=False,
        label="  ¿Hay expediente físico?",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'style': '',
            'style': 'transform: scale(1.5); cursor: pointer; box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); border: 1px solid rgba(128, 128, 128, 1);',
            
        }),
    )
    
    cuij = forms.CharField(
        label="Código Único de Identificación Judicial:",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    clave_sisfe = forms.CharField(
        label = "SISFE, o Sistema Integrado de Consultas Judiciales",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    observaciones = forms.CharField(
        label="Observaciones:",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    #Con esta función obtenemos la sede asignada al usuario para cargar el formulario
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtenemos el usuario desde la vista
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated and hasattr(user, 'sede'):
            self.fields['sede'].initial = user.sede  # Valor inicial
            self.fields['sede'].queryset = Sede.objects.filter(id=user.sede.id)  # Solo su sede
            self.fields['sede'].disabled = True  # Opcional: para que no pueda cambiarla