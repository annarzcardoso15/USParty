from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ingressos.models import Anuncio
from .forms import InteresseForm
from .models import ManifestarInteresse

# Enquanto não existe tela de login, usamos o login do admin
@login_required(login_url='/admin/login/')
def manifestar_interesse(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    erro = None

    if request.method == 'POST':
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

                # Trocar para a Tela 12 quando ela existir
                return redirect('minhas_compras')
    else:
        form = InteresseForm()

    return render(request, 'negociacoes/manifestar_interesse.html', {'form': form, 'anuncio': anuncio, 'erro': erro})

@login_required(login_url='/admin/login/')
def minhas_compras(request):
    interesses = ManifestarInteresse.objects.filter(pessoal=request.user.pessoal).order_by('-id_interesse')
    return render(request, 'negociacoes/minhas_compras.html', {'interesses': interesses})