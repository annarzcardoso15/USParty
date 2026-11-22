from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

                return redirect('minhas_compras')
    else:
        form = InteresseForm()

    return render(request, 'negociacoes/manifestar_interesse.html', {'form': form, 'anuncio': anuncio, 'erro': erro})


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