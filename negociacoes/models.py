from django.db import models
from usuarios.models import Pessoal
from ingressos.models import Anuncio

class ManifestarInteresse(models.Model):
    id_interesse = models.AutoField(primary_key=True)
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE)
    pessoal = models.ForeignKey(Pessoal, on_delete=models.CASCADE) 
    
    quantidade_desejada = models.IntegerField()
    concorda_valor = models.BooleanField(default=False)

    def __str__(self):
        return f"Interesse de {self.pessoal.nome} no anúncio {self.anuncio.id_anuncio}"