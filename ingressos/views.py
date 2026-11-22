# Criar página de criar anuncios, vitrine dos ingressos e meus anuncios.
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Anuncio, Festa, Pessoal
from .forms import Etapa1Form, Etapa2Form
from django.forms import formset_factory
from django.contrib.auth import get_user_model
from .models import Anuncio, Festa, Status
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def criar_etapa1(request):
    if request.method == 'POST':
        form = Etapa1Form(request.POST)
        if form.is_valid():
            festa_selecionada = form.cleaned_data['festa']
            quantidade = form.cleaned_data['quantidade']

            request.session['festa_id'] = festa_selecionada.idfesta
            request.session['quantidade_ingressos'] = quantidade
            

            return redirect('criar_etapa2') 
    else:
        form = Etapa1Form()
        
    return render(request, 'ingressos/etapa1.html', {'form': form})

@login_required(login_url='login')
def criar_etapa2(request):
    quantidade = request.session.get('quantidade_ingressos', 1)
    AnuncioFormSet = formset_factory(Etapa2Form, extra=quantidade)

    if request.method == 'POST':
        formset = AnuncioFormSet(request.POST)

        if formset.is_valid():
            festa_id = request.session.get('festa_id')
            festa = get_object_or_404(Festa, idfesta=festa_id)

            for form in formset:
                if form.has_changed():
                    anuncio = form.save(commit=False)
                    anuncio.festa = festa
                    anuncio.pessoal = request.user.pessoal
                    anuncio.status = Status.objects.create()
                    anuncio.save()


            if 'festa_id' in request.session:
                del request.session['festa_id']
            if 'quantidade_ingressos' in request.session:
                del request.session['quantidade_ingressos']

            return redirect('catalogo_ingressos', festa_id=festa_id)
    else:
        formset = AnuncioFormSet()

    return render(request, 'ingressos/etapa2.html', {'formset': formset})

def catalogo_ingressos(request, festa_id):
    festa = get_object_or_404(Festa, idfesta=festa_id)
    
    anuncios = Anuncio.objects.filter(festa=festa, status__vendido=False).order_by('-status__disponivel', '-status__em_negociacao')
    
    context = {
        'festa': festa,
        'anuncios': anuncios
    }

    return render(request, 'ingressos/catalogo_ingressos.html', context)

@login_required(login_url='login')
def meus_anuncios(request):
    pessoal_teste = Pessoal.objects.first()
    

    anuncios = Anuncio.objects.filter(pessoal=request.user.pessoal)
    
    context = {
        'anuncios': anuncios
    }
    return render(request, 'ingressos/meus_anuncios.html', context)

@login_required(login_url='login')
def editar_anuncio(request, id_anuncio):
    # Puxa o anúncio garantindo que é do utilizador
    anuncio = get_object_or_404(Anuncio, id_anuncio=id_anuncio, pessoal=request.user.pessoal)
    
    if request.method == 'POST':
        # Salva o novo preço
        novo_preco = request.POST.get('preco')
        if novo_preco:
            anuncio.preco = novo_preco
        
        # Salva o novo status
        novo_status = request.POST.get('status_escolhido')
        status = anuncio.status
        if novo_status == 'disponivel':
            status.disponivel = True
            status.em_negociacao = False
            status.vendido = False
        elif novo_status == 'em_negociacao':
            status.disponivel = False
            status.em_negociacao = True
            status.vendido = False
        elif novo_status == 'vendido':
            status.disponivel = False
            status.em_negociacao = False
            status.vendido = True
            
        status.save()
        anuncio.save()
        
        # Redireciona de volta para a lista
        return redirect('meus_anuncios')
        
    return render(request, 'ingressos/editar_anuncio.html', {'anuncio': anuncio})

@login_required(login_url='login')
def atualizar_status(request, id_anuncio):
    anuncio = get_object_or_404(Anuncio, id_anuncio=id_anuncio, pessoal=request.user.pessoal)
    if request.method == 'POST':
        novo_status = request.POST.get('status_escolhido')
        status = anuncio.status
        
        # Atualiza os booleanos conforme a escolha
        if novo_status == 'disponivel':
            status.disponivel = True
            status.em_negociacao = False
            status.vendido = False
        elif novo_status == 'em_negociacao':
            status.disponivel = False
            status.em_negociacao = True
            status.vendido = False
        elif novo_status == 'vendido':
            status.disponivel = False
            status.em_negociacao = False
            status.vendido = True
            
        status.save()
    return redirect('meus_anuncios')

@login_required(login_url='login')
def excluir_anuncio(request, id_anuncio):
    anuncio = get_object_or_404(Anuncio, id_anuncio=id_anuncio, pessoal=request.user.pessoal)
    if request.method == 'POST':
        anuncio.delete()
    return redirect('meus_anuncios')