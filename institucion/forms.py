from django import forms
from .models import Institucion, TipoInstitucion

class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = [
            'institucion', 
            'tipo_institucion', 
            'domicilio_calle', 
            'domicilio_numero', 
            'domicilio_piso', 
            'localidad', 
            'telefono', 
            'email', 
            'cuit', 
            'estado'
        ]
        
        widgets = {
            'institucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la institución'}),
            'tipo_institucion': forms.Select(attrs={'class': 'form-control'}),
            'domicilio_calle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la calle'}),
            'domicilio_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número'}),
            'domicilio_piso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el piso'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el CUIT'}),
        }
    
    def clean_institucion(self):
        institucion = self.cleaned_data.get('institucion')
        if not institucion:
            raise forms.ValidationError('Este campo es obligatorio.')
        return institucion
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institucion'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_institucion'].widget.attrs.update({'class': 'form-control'})
        self.fields['domicilio_calle'].widget.attrs.update({'class': 'form-control'})
        self.fields['domicilio_numero'].widget.attrs.update({'class': 'form-control'})
        self.fields['domicilio_piso'].widget.attrs.update({'class': 'form-control'})
        self.fields['localidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['cuit'].widget.attrs.update({'class': 'form-control'})      