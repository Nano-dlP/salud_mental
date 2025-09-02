from django import forms
from django.contrib.auth import get_user_model
from .models import Profesional
from django.db.models import Q
User = get_user_model()


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['user', 'profesion', 'area_profesional', 'estado']
        labels = {
            'user': 'Usuario',
            'profesion': 'Profesión',
            'area_profesional': 'Área profesional',
            'estado': 'Estado',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'profesion': forms.Select(attrs={'class': 'form-control'}),
            'area_profesional': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir usuarios ya asociados a un profesional
        # ⚠️ Si estamos editando, incluir al usuario actual
        if self.instance and self.instance.pk:
            self.fields['user'].queryset = User.objects.filter(
                Q(profesional_usuario__isnull=True) | Q(pk=self.instance.user.pk)
            )
        else:
            self.fields['user'].queryset = User.objects.filter(profesional_usuario__isnull=True)

        # Mostrar nombre completo
        self.fields['user'].label_from_instance = lambda obj: obj.get_full_name() or obj.username
    