from django import forms
from .models import Institucion, TipoInstitucion
import re


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = [
            'institucion',
            'tipo_institucion',
            'domicilio_calle',
            'domicilio_numero',
            'domicilio_piso',
            'domicilio_depto',
            'localidad',
            'telefono',
            'email',
            'cuit',
            'estado',
        ]

        widgets = {
            'institucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la institución'}),
            'tipo_institucion': forms.Select(attrs={'class': 'form-control'}),
            'domicilio_calle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la calle'}),
            'domicilio_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número'}),
            'domicilio_piso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el piso'}),
            'domicilio_depto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el departamento'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el CUIT'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'institucion': 'Institución',
            'tipo_institucion': 'Tipo de Institución',
            'domicilio_calle': 'Calle',
            'domicilio_numero': 'Número',
            'domicilio_piso': 'Piso',
            'domicilio_depto': 'Departamento',
            'localidad': 'Localidad',
            'telefono': 'Teléfono',
            'email': 'Email',
            'cuit': 'CUIT',
            'estado': 'Activo',
        }

    def clean_institucion(self):
        institucion = self.cleaned_data.get('institucion')
        if not institucion:
            raise forms.ValidationError('Este campo es obligatorio.')
        if len(institucion) < 3:
            raise forms.ValidationError('El nombre de la institución debe tener al menos 3 caracteres.')
        return institucion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')
        return telefono

    def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')
        if not cuit:
            raise forms.ValidationError("Este campo es obligatorio.")
        if not re.match(r'^\d{2}-\d{8}-\d$', cuit):
            raise forms.ValidationError("CUIT inválido. Debe tener el formato XX-XXXXXXXX-X")
        return cuit
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra solo localidades activas
        #self.fields['localidad'].queryset = Localidad.objects.filter(estado=True)
        self.fields['tipo_institucion'].queryset = TipoInstitucion.objects.filter(estado=True)


    def clean(self):
        cleaned_data = super().clean()

        # Transformación de valores de texto
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                if field_name == 'email':
                    cleaned_data[field_name] = value.lower()  # Email en minúsculas
                else:
                    cleaned_data[field_name] = value.upper()  # Todo lo demás en mayúsculas

        return cleaned_data