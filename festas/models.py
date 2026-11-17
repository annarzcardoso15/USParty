from django.db import models
from usuarios.models import Adm, Instituicao, Pessoal 

class Festa(models.Model):
    idfesta = models.AutoField(primary_key=True)
    adm = models.ForeignKey(Adm, on_delete=models.CASCADE) 
    nome_festa = models.CharField(max_length=255)
    data_festa = models.DateField()
    lotes = models.CharField(max_length=255)
    tipo_ingresso_disponivel = models.CharField(max_length=255)
    
    organizadores = models.ManyToManyField(Instituicao, related_name='festas_organizadas')
    vendedores_oficiais = models.ManyToManyField(Pessoal, related_name='festas_oficiais', blank=True)
    def __str__(self):
        return self.nome_festa