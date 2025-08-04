from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = [  'tipo_documento',
                    'numero_documento','nombre',
                    'apellido', 'fecha_nacimiento',
                    'genero', 'telefono', 'email',
                    'direccion_calle', 'direccion_numero',
                    'direccion_piso', 'direccion_depto',
                    'localidad', 'ciudad_nacimiento',
                    'nivel_educativo', 'ocupacion',
                    'posee_cobertura_salud', 'cobertura_salud',
                    'posee_grupo_apoyo', 'grupo_apoyo',
                    'derecho_seguridad_social', 'administra_recursos',
                    'carnet_discapacidad', 'situacion_habitacional',
                    'observaciones']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de documento'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'direccion_calle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la calle'}),
            'direccion_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número'}),
            'direccion_piso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el piso'}),
            'direccion_depto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el departamento'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'ciudad_nacimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ciudad de nacimiento'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ocupación'}),
            'posee_cobertura_salud': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cobertura_salud': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cobertura de salud'}),
            'posee_grupo_apoyo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'grupo_apoyo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el grupo de apoyo'}),
            'derecho_seguridad_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el derecho a la seguridad social'}),
            'administra_recursos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'carnet_discapacidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el carnet de discapacidad'}),
            'situacion_habitacional': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la situación habitacional'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese observaciones', 'rows': 3}),
        }