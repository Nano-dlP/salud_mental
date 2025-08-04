from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'tipo_documento', 'numero_documento', 'nombre', 'apellido', 'fecha_nacimiento',
            'genero', 'telefono', 'email', 'direccion_calle', 'direccion_numero',
            'direccion_piso', 'direccion_depto', 'localidad', 'ciudad_nacimiento',
            'nivel_educativo', 'ocupacion', 'posee_cobertura_salud', 'cobertura_salud',
            'posee_grupo_apoyo', 'grupo_apoyo', 'derecho_seguridad_social',
            'administra_recursos', 'carnet_discapacidad', 'situacion_habitacional',
            'observaciones'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_calle': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_numero': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_piso': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_depto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'localidad': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'ciudad_nacimiento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'posee_cobertura_salud': forms.CheckboxInput(attrs={'class': 'form-check-input form-check-input-sm'}),
            'cobertura_salud': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'posee_grupo_apoyo': forms.CheckboxInput(attrs={'class': 'form-check-input form-check-input-sm'}),
            'grupo_apoyo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'derecho_seguridad_social': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'administra_recursos': forms.CheckboxInput(attrs={'class': 'form-check-input form-check-input-sm'}),
            'carnet_discapacidad': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'situacion_habitacional': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("posee_cobertura_salud") and not cleaned_data.get("cobertura_salud"):
            self.add_error("cobertura_salud", "Debe indicar la cobertura de salud si posee una.")



    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("posee_grupo_apoyo") and not cleaned_data.get("grupo_apoyo"):
            self.add_error("grupo_apoyo", "Debe indicar el grupo de apoyo si posee uno.")
            
            
    # forms.py

    def clean(self):
        cleaned_data = super().clean()

        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                if field_name == 'email':
                    cleaned_data[field_name] = value.lower()  # Email en minúsculas
                elif field_name == 'observaciones':
                    cleaned_data[field_name] = value  # Observaciones sin alterar
                else:
                    cleaned_data[field_name] = value.upper()  # Todo lo demás en mayúsculas

        return cleaned_data