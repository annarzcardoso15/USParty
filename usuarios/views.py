from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pessoal, Instituicao, Adm
from .forms import CadastroPessoalForm, CadastroInstituicaoForm, LoginForm
from ingressos.models import Anuncio
from festas.models import Festa
from negociacoes.models import ManifestarInteresse


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
    is_adm = Adm.objects.filter(usuario=user).exists() or user.is_superuser or user.is_staff
    if is_adm and not Adm.objects.filter(usuario=user).exists():
        Adm.objects.create(usuario=user)

    # Ação exclusiva de Admin: promover usuário existente a Administrador
    if request.method == 'POST' and is_adm and 'promover_admin' in request.POST:
        identificador = request.POST.get('identificador_admin', '').strip()
        alvo = User.objects.filter(email=identificador).first() or User.objects.filter(username=identificador).first()
        if not alvo:
            messages.error(request, f"Usuário '{identificador}' não encontrado.")
        elif Adm.objects.filter(usuario=alvo).exists():
            messages.warning(request, f"O usuário '{alvo.username}' já é administrador.")
        else:
            Adm.objects.create(usuario=alvo)
            alvo.is_staff = True
            alvo.save()
            messages.success(request, f"Usuário '{alvo.username}' promovido a Administrador com sucesso!")
        return redirect('perfil')

    # Ação exclusiva de Instituição: gerenciar vendedores oficiais da própria festa
    if request.method == 'POST' and perfil_instituicao:
        if 'adicionar_vendedor' in request.POST:
            festa_id = request.POST.get('festa_id')
            identificador = request.POST.get('identificador_vendedor', '').strip()
            
            festa = perfil_instituicao.festas_organizadas.filter(idfesta=festa_id).first()
            user_alvo = User.objects.filter(email=identificador).first() or User.objects.filter(username=identificador).first()
            pessoal_alvo = Pessoal.objects.filter(usuario=user_alvo).first() if user_alvo else None

            if not festa:
                messages.error(request, "Festa não encontrada ou não pertence a esta instituição.")
            elif not pessoal_alvo:
                messages.error(request, f"Nenhuma conta pessoal encontrada com '{identificador}'.")
            elif festa.vendedores_oficiais.filter(pk=pessoal_alvo.pk).exists():
                messages.warning(request, f"{pessoal_alvo.nome} já é vendedor(a) oficial desta festa.")
            else:
                festa.vendedores_oficiais.add(pessoal_alvo)
                messages.success(request, f"{pessoal_alvo.nome} adicionado(a) como vendedor(a) oficial de {festa.nome_festa}!")
            return redirect('perfil')

        elif 'remover_vendedor' in request.POST:
            festa_id = request.POST.get('festa_id')
            vendedor_id = request.POST.get('vendedor_id')
            festa = perfil_instituicao.festas_organizadas.filter(idfesta=festa_id).first()
            pessoal_alvo = Pessoal.objects.filter(pk=vendedor_id).first()

            if festa and pessoal_alvo:
                festa.vendedores_oficiais.remove(pessoal_alvo)
                messages.success(request, f"{pessoal_alvo.nome} removido(a) dos vendedores oficiais.")
            return redirect('perfil')

    contexto = {
        'perfil_pessoal': perfil_pessoal,
        'perfil_instituicao': perfil_instituicao,
        'is_adm': is_adm,
    }

    # USP011: Totalização Pessoal (Vendas + Compras/Interesses)
    if perfil_pessoal:
        meus_anuncios = Anuncio.objects.filter(pessoal=perfil_pessoal).select_related('festa', 'status')
        disponiveis = meus_anuncios.filter(status__disponivel=True, status__vendido=False, status__em_negociacao=False)
        em_negociacao = meus_anuncios.filter(status__em_negociacao=True)
        vendidos = meus_anuncios.filter(status__vendido=True)

        valor_vendido = sum(a.preco * a.quantidade_ingressos for a in vendidos)
        valor_ativo = sum(a.preco * a.quantidade_ingressos for a in disponiveis) + sum(a.preco * a.quantidade_ingressos for a in em_negociacao)

        meus_interesses = ManifestarInteresse.objects.filter(pessoal=perfil_pessoal).select_related('anuncio', 'anuncio__festa', 'anuncio__status')
        qtd_ingressos_comprados = sum(i.quantidade_desejada for i in meus_interesses)
        valor_total_compras = sum(i.quantidade_desejada * i.anuncio.preco for i in meus_interesses)

        contexto.update({
            'meus_anuncios': meus_anuncios,
            'meus_interesses': meus_interesses,
            'usp011': {
                'total_anuncios': meus_anuncios.count(),
                'qtd_disponiveis': disponiveis.count(),
                'qtd_negociacao': em_negociacao.count(),
                'qtd_vendidos': vendidos.count(),
                'valor_vendido': valor_vendido,
                'valor_ativo': valor_ativo,
                'total_interesses': meus_interesses.count(),
                'qtd_ingressos_comprados': qtd_ingressos_comprados,
                'valor_total_compras': valor_total_compras,
            }
        })

    # USP012: Totalização de Atlética / Instituição
    elif perfil_instituicao:
        festas_inst = perfil_instituicao.festas_organizadas.all().order_by('data_festa')
        resumo_festas = []
        total_anuncios_inst = 0
        total_vendidos_inst = 0
        receita_total_inst = 0.0

        for festa in festas_inst:
            anuncios_festa = Anuncio.objects.filter(festa=festa).select_related('status')
            vendidos_festa = anuncios_festa.filter(status__vendido=True)
            disponiveis_festa = anuncios_festa.filter(status__disponivel=True, status__vendido=False)
            volume_festa = sum(a.preco * a.quantidade_ingressos for a in vendidos_festa)

            total_anuncios_inst += anuncios_festa.count()
            total_vendidos_inst += vendidos_festa.count()
            receita_total_inst += volume_festa

            resumo_festas.append({
                'festa': festa,
                'total_anuncios': anuncios_festa.count(),
                'disponiveis': disponiveis_festa.count(),
                'vendidos': vendidos_festa.count(),
                'volume_financeiro': volume_festa,
            })

        contexto.update({
            'usp012': {
                'total_festas': festas_inst.count(),
                'total_anuncios': total_anuncios_inst,
                'total_vendidos': total_vendidos_inst,
                'receita_total': receita_total_inst,
                'resumo_festas': resumo_festas,
            }
        })

    # USP013: Totalização Geral (Administrador)
    elif is_adm:
        todos_anuncios = Anuncio.objects.select_related('status', 'festa')
        vendidos_geral = todos_anuncios.filter(status__vendido=True)
        disponiveis_geral = todos_anuncios.filter(status__disponivel=True, status__vendido=False, status__em_negociacao=False)
        negociacao_geral = todos_anuncios.filter(status__em_negociacao=True)
        volume_geral = sum(a.preco * a.quantidade_ingressos for a in vendidos_geral)

        contexto.update({
            'usp013': {
                'total_pessoal': Pessoal.objects.count(),
                'total_instituicoes': Instituicao.objects.count(),
                'total_admins': Adm.objects.count(),
                'total_festas': Festa.objects.count(),
                'total_anuncios': todos_anuncios.count(),
                'anuncios_disponiveis': disponiveis_geral.count(),
                'anuncios_negociacao': negociacao_geral.count(),
                'anuncios_vendidos': vendidos_geral.count(),
                'total_negociacoes': ManifestarInteresse.objects.count(),
                'volume_transacionado': volume_geral,
            }
        })

    return render(request, 'usuarios/perfil.html', contexto)