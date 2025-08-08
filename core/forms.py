from django import forms
from .models import Localidad
from datetime import date
from .models import Provincia

class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        fields = ['provincia', 'pais']
        
        widgets = {
            'provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la provincia'
            }),
            'pais': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un país'
            }),
        }
    
    def clean_provincia(self):
        provincia = self.cleaned_data.get('provincia')
        if not provincia:
            raise forms.ValidationError('Este campo es obligatorio.')
        return provincia
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provincia'].widget.attrs.update({'class': 'form-control'})