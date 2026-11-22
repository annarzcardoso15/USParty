from django.db import models
from usuarios.models import Pessoal
from festas.models import Festa


class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    disponivel = models.BooleanField(default=True)
    em_negociacao = models.BooleanField(default=False)
    vendido = models.BooleanField(default=False)

    def __str__(self):
        if self.vendido: return "Vendido"
        if self.em_negociacao: return "Em Negociação"
        return "Disponível"


class Anuncio(models.Model):
    id_anuncio = models.AutoField(primary_key=True)
    festa = models.ForeignKey(Festa, on_delete=models.CASCADE)
    pessoal = models.ForeignKey(Pessoal, on_delete=models.CASCADE) 
    

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    quantidade_ingressos = models.IntegerField(default=1, verbose_name="Quantidade")
    lote = models.CharField(max_length=255)
    preco = models.FloatField()
    
    tipo_ingresso = models.BooleanField(help_text="Marque se for aluno usp, desmarque se for nao aluno")

    def __str__(self):
        return f"Ingresso {self.festa.nome_festa} - {self.pessoal.nome}"