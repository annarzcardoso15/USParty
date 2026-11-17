from django import forms
from .models import Anuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['festa', 'preco', 'lote'] 
        widgets = {
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
        }