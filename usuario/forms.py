from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



User = get_user_model()

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'telefono', 'direccion', 'foto_perfil']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'foto_perfil', 'is_staff']

class CustomUserUpdateForm(UserChangeForm):
    password = None  # opcional, si no querés mostrar el campo contraseña

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'foto_perfil', 'is_staff']
