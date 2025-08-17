from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'dni', 'telefono', 'direccion', 'localidad', 'sede', 'foto_perfil']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:
            raise ValidationError("El campo DNI no puede estar vacío.")
        
        # Si es edición (el usuario ya existe), excluimos su propio ID
        if CustomUser.objects.filter(dni=dni).exclude(id=self.instance.id).exists():
            raise ValidationError("Ya existe un usuario con ese DNI.")
        
        return dni
