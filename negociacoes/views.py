from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ingressos.models import Anuncio
from .forms import InteresseForm
from .models import ManifestarInteresse


@login_required(login_url='login')
def manifestar_interesse(request, anuncio_id):
    # Só quem tem cadastro de pessoa pode comprar
    if not hasattr(request.user, 'pessoal'):
        return render(request, 'negociacoes/sem_conta_pessoal.html')

    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    erro = None

    # USP007 exige anúncio "Disponível"
    if not anuncio.status.disponivel:
        erro = 'Esse anúncio não está mais disponível.'
    # Não pode manifestar interesse no próprio anúncio
    elif anuncio.pessoal == request.user.pessoal:
        erro = 'Esse anúncio é seu!'
    # Não pode manifestar interesse duas vezes no mesmo anúncio
    elif ManifestarInteresse.objects.filter(anuncio=anuncio, pessoal=request.user.pessoal).exists():
        erro = 'Você já manifestou interesse nesse anúncio. Para mudar a quantidade, desista em Minhas Compras e faça de novo.'

    # Se já existe um erro aqui, o formulário nem aparece na tela
    bloqueado = erro is not None

    if request.method == 'POST' and erro is None:
        form = InteresseForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade_desejada']
            if quantidade > anuncio.quantidade_ingressos:
                erro = 'Esse anúncio só tem ' + str(anuncio.quantidade_ingressos) + ' ingresso(s).'
            else:
                interesse = form.save(commit=False)
                interesse.anuncio = anuncio
                interesse.pessoal = request.user.pessoal
                interesse.save()

                # USP007: diminui a quantidade; se acabar, fica "Em negociação"
                anuncio.quantidade_ingressos = anuncio.quantidade_ingressos - quantidade
                anuncio.save()
                if anuncio.quantidade_ingressos == 0:
                    anuncio.status.disponivel = False
                    anuncio.status.em_negociacao = True
                    anuncio.status.save()

                messages.success(request, 'Interesse registrado! Agora é só chamar o vendedor no WhatsApp.')
                return redirect('minhas_compras')
    else:
        form = InteresseForm()

    return render(request, 'negociacoes/manifestar_interesse.html', {'form': form, 'anuncio': anuncio, 'erro': erro, 'bloqueado': bloqueado})


@login_required(login_url='login')
def minhas_compras(request):
    if not hasattr(request.user, 'pessoal'):
        return render(request, 'negociacoes/sem_conta_pessoal.html')
    interesses = ManifestarInteresse.objects.filter(pessoal=request.user.pessoal).order_by('-id_interesse')
    return render(request, 'negociacoes/minhas_compras.html', {'interesses': interesses})


@login_required(login_url='login')
def interessados(request):
    if not hasattr(request.user, 'pessoal'):
        return render(request, 'negociacoes/sem_conta_pessoal.html')
    interesses = ManifestarInteresse.objects.filter(anuncio__pessoal=request.user.pessoal).order_by('-id_interesse')
    return render(request, 'negociacoes/interessados.html', {'interesses': interesses})


@login_required(login_url='login')
def desistir_interesse(request, id_interesse):
    if not hasattr(request.user, 'pessoal'):
        return render(request, 'negociacoes/sem_conta_pessoal.html')

    # Só a própria pessoa pode desistir do interesse dela
    interesse = get_object_or_404(ManifestarInteresse, pk=id_interesse, pessoal=request.user.pessoal)
    anuncio = interesse.anuncio

    # Só aceita POST (o botão é um formulário) e não vale para anúncio já vendido
    if request.method == 'POST' and not anuncio.status.vendido:
        # Se o anúncio tinha esgotado por causa dos interesses, ele volta a ficar disponível
        if anuncio.quantidade_ingressos == 0 and anuncio.status.em_negociacao:
            anuncio.status.disponivel = True
            anuncio.status.em_negociacao = False
            anuncio.status.save()

        # Os ingressos pedidos voltam para o anúncio
        anuncio.quantidade_ingressos = anuncio.quantidade_ingressos + interesse.quantidade_desejada
        anuncio.save()
        interesse.delete()
        messages.success(request, 'Você desistiu do ingresso. Os ingressos voltaram para o anúncio.')

    return redirect('minhas_compras')