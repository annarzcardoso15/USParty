from django import forms
from .models import ManifestarInteresse

class InteresseForm(forms.ModelForm):
    class Meta:
        model = ManifestarInteresse
        fields = ['quantidade_desejada', 'concorda_valor']
        labels = {
            'quantidade_desejada': 'Quantidade de ingressos',
            'concorda_valor': 'Concordo com o valor anunciado (desmarque se quiser negociar)',
        }
        widgets = {
            'quantidade_desejada': forms.NumberInput(attrs={'min': 1}),
        }