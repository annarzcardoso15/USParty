from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pessoal, Instituicao, Adm
from .forms import CadastroPessoalForm, CadastroInstituicaoForm, LoginForm
from ingressos.models import Anuncio

def cadastro_view(request):
    tipo = request.POST.get('tipo_conta', 'pessoal')
    form_pessoal = CadastroPessoalForm()
    form_instituicao = CadastroInstituicaoForm()

    if request.method == 'POST':
        if tipo == 'pessoal':
            form_pessoal = CadastroPessoalForm(request.POST)
            if form_pessoal.is_valid():
                dados = form_pessoal.cleaned_data
                user = User.objects.create_user(
                    username=dados['username'],
                    email=dados['email'],
                    password=dados['senha']
                )
                inst = 'USP' if dados['vinculo'] == 'usp' else (dados['instituicao'] or 'Não-aluno / Externa')
                Pessoal.objects.create(
                    usuario=user,
                    nome=dados['nome'],
                    cpf=dados['cpf'],
                    telefone=dados['telefone'],
                    data_nascimento=dados['data_nascimento'],
                    instituicao=inst
                )
                messages.success(request, "Cadastro realizado com sucesso! Faça seu login.")
                return redirect('login')
        elif tipo == 'instituicao':
            form_instituicao = CadastroInstituicaoForm(request.POST)
            if form_instituicao.is_valid():
                dados = form_instituicao.cleaned_data
                user = User.objects.create_user(
                    username=dados['email'],
                    email=dados['email'],
                    password=dados['senha']
                )
                Instituicao.objects.create(
                    usuario=user,
                    nome=dados['nome'],
                    cnpj=dados['cnpj'],
                    telefone=dados['telefone']
                )
                messages.success(request, "Instituição cadastrada com sucesso! Faça seu login.")
                return redirect('login')

    return render(request, 'usuarios/cadastro.html', {
        'form_pessoal': form_pessoal,
        'form_instituicao': form_instituicao,
        'tipo_ativo': tipo
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identificador = form.cleaned_data['identificador']
        senha = form.cleaned_data['senha']

        user_obj = User.objects.filter(email=identificador).first() or User.objects.filter(username=identificador).first()

        if user_obj:
            if not user_obj.is_active:
                messages.error(request, "Sua conta encontra-se temporariamente inativa. Entre em contato com a USParty.")
                return render(request, 'usuarios/login.html', {'form': form})

            user = authenticate(request, username=user_obj.username, password=senha)
            if user is not None:
                login(request, user)
                return redirect('perfil')

        messages.error(request, "E-mail/usuário ou senha incorretos. Verifique os dados e tente novamente.")

    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def perfil_view(request):
    user = request.user
    perfil_pessoal = Pessoal.objects.filter(usuario=user).first()
    perfil_instituicao = Instituicao.objects.filter(usuario=user).first()
    is_adm = Adm.objects.filter(usuario=user).exists()

    meus_anuncios = []
    if perfil_pessoal:
        meus_anuncios = Anuncio.objects.filter(pessoal=perfil_pessoal)

    return render(request, 'usuarios/perfil.html', {
        'perfil_pessoal': perfil_pessoal,
        'perfil_instituicao': perfil_instituicao,
        'is_adm': is_adm,
        'meus_anuncios': meus_anuncios,
    })