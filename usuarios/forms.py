from django import forms
from django.contrib.auth.models import User
from .models import Pessoal, Instituicao

class CadastroPessoalForm(forms.Form):
    VINCULO_CHOICES = [
        ('usp', 'Aluno USP'),
        ('externo', 'Não-aluno / Outra Instituição'),
    ]

    vinculo = forms.ChoiceField(
        label="Vínculo Estudantil",
        choices=VINCULO_CHOICES,
        widget=forms.Select,
        initial='usp'
    )
    nome = forms.CharField(label="Nome completo", max_length=255)
    username = forms.CharField(label="Nome de usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    cpf = forms.IntegerField(label="CPF (apenas números)")
    data_nascimento = forms.DateField(
        label="Data de nascimento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    telefone = forms.IntegerField(label="Telefone (com DDD, apenas números)")
    instituicao = forms.CharField(
        label="Qual instituição? (se não for USP)",
        max_length=255,
        required=False
    )
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já possui cadastro.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Pessoal.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já possui cadastro.")
        return cpf


class CadastroInstituicaoForm(forms.Form):
    nome = forms.CharField(label="Nome da instituição / atlética", max_length=255)
    email = forms.EmailField(label="E-mail institucional")
    cnpj = forms.IntegerField(label="CNPJ (apenas números)")
    telefone = forms.IntegerField(label="Telefone (com DDD, apenas números)")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já possui cadastro.")
        return email

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        if Instituicao.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError("Este CNPJ já possui cadastro.")
        return cnpj


class LoginForm(forms.Form):
    identificador = forms.CharField(label="E-mail ou nome de usuário")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)