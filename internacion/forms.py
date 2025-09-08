from django import forms
from .models import Internacion


class InternacionForm(forms.ModelForm):
    class Meta:
        model = Internacion
        fields = ['expediente_institucion', 
                  'fecha_internacion', 
                  'fecha_alta', 
                  'motivo_internacion', 
                  'motivo_alta', 
                  'requisitos', 
                  'intento_suicidio', 
                  'modalidad_suicidio', 
                  'posse_adiccion', 
                  'tipo_adiccion', 
                  'fecha_cumplimiento']
        
        widgets = {
            'expediente_institucion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'fecha_internacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_alta': forms.DateInput(attrs={'type': 'date'}),
            'motivo_internacion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'motivo_alta': forms.Select(attrs={'class': 'form-control form-control-sm   '}),
            'requisitos': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Requisitos'}),
            'intento_suicidio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'modalidad_suicidio': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'posse_adiccion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_adiccion': forms.Select(attrs={'class': 'form-control form-control-sm'}), 
            'fecha_cumplimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'expediente_institucion': 'Expediente Institución',
            'fecha_internacion': 'Fecha de internación',
            'fecha_alta': 'Fecha de alta',
            'motivo_internacion': 'Motivo de internación',
            'motivo_alta': 'Motivo de alta',
            'requisitos': 'Requisitos',
            'intento_suicidio': 'Intento de suicidio',
            'modalidad_suicidio': 'Modalidad de suicidio',
            'posse_adiccion': 'Posee adicción',
            'tipo_adiccion': 'Tipo de adicción',
            'fecha_cumplimiento': 'Fecha de cumplimiento',
        }
        
    def clean_fecha_alta(self):
        fecha_internacion = self.cleaned_data.get('fecha_internacion')
        fecha_alta = self.cleaned_data.get('fecha_alta')
        
        if fecha_internacion and fecha_alta:
            if fecha_alta < fecha_internacion:
                raise forms.ValidationError("⚠️ La fecha de alta no puede ser anterior a la fecha de internación.")
        
        return fecha_alta
    
    def clean_fecha_cumplimiento(self):
        fecha_cumplimiento = self.cleaned_data.get('fecha_cumplimiento')
        fecha_internacion = self.cleaned_data.get('fecha_internacion')
        fecha_alta = self.cleaned_data.get('fecha_alta')
        
        if fecha_cumplimiento:
            if fecha_internacion and fecha_cumplimiento < fecha_internacion:
                raise forms.ValidationError("⚠️ La fecha de cumplimiento no puede ser anterior a la fecha de internación.")
            if fecha_alta and fecha_cumplimiento < fecha_alta:
                raise forms.ValidationError("⚠️ La fecha de cumplimiento no puede ser anterior a la fecha de alta.")
        
        return fecha_cumplimiento
    
        