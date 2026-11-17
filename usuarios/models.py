from django.db import models
from django.contrib.auth.models import User

class Pessoal(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.BigIntegerField(unique=True)
    telefone = models.BigIntegerField()
    data_nascimento = models.DateField()
    instituicao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Instituicao(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=255)
    cnpj = models.BigIntegerField(unique=True)
    telefone = models.BigIntegerField()

    def __str__(self):
        return self.nome

class Adm(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.username
# Create your models here.
