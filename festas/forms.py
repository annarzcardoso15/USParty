from django import forms
from .models import Festa

class FestaForm(forms.ModelForm):
    class Meta:
        model = Festa
        fields = ['nome_festa', 'data_festa', 'imagem',  'lotes', 'tipo_ingresso_disponivel', 'organizadores', 'vendedores_oficiais'] 
        

        widgets = {
            'data_festa': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}), 
            'imagem': forms.URLInput(attrs={'placeholder': 'https://exemplo.com/foto-da-festa.jpg'}),
            'organizadores': forms.CheckboxSelectMultiple(),
            'vendedores_oficiais': forms.CheckboxSelectMultiple(),
        }