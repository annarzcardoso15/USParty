from django import forms
from .models import Festa

class FestaForm(forms.ModelForm):
    class Meta:
        model = Festa
        fields = ['adm','nome_festa', 'data_festa', 'lotes', 'tipo_ingresso_disponivel', 'organizadores'] #quando criar login, tirar esse adm!!!
        

        widgets = {
            'data_festa': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        }