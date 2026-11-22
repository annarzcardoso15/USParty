from django import forms
from .models import Anuncio

#Etapa 1 : quantidade de ingressos e festa
class Etapa1Form(forms.ModelForm):
    quantidade = forms.IntegerField(
        min_value=1, 
        max_value=20, 
        label='Quantidade de Ingressos a vender'
    )

    class Meta:
        model = Anuncio
        fields = ['festa'] 
        labels = {'festa': 'Selecione a Festa'}

#Etapa 2 : lote e preço de cada ingresso
class Etapa2Form(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['lote', 'tipo_ingresso', 'preco']
        labels = {
            'lote': 'Lote do Ingresso',
            'preco': 'Preço',
            'tipo_ingresso': 'Tipo de Ingresso'
        }
        widgets = {
                    'preco': forms.NumberInput(attrs={'step': '0.01'}),
                    'tipo_ingresso': forms.Select(choices=[
                        (True, 'Aluno USP'),
                        (False, 'Não Aluno')
                    ]),
        }
        