# Criar página de criar anuncios, vitrine dos ingressos e meus anuncios.
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Anuncio, Festa, Pessoal
from .forms import Etapa1Form, Etapa2Form
from django.forms import formset_factory
from django.contrib.auth import get_user_model

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

def criar_etapa2(request):
    quantidade = request.session.get('quantidade_ingressos', 1)
    
    AnuncioFormSet = formset_factory(Etapa2Form, extra=quantidade)
    
    if request.method == 'POST':
        formset = AnuncioFormSet(request.POST)
        if formset.is_valid():
            festa_id = request.session.get('festa_id')
            festa = get_object_or_404(Festa, idfesta=festa_id)
            

            User = get_user_model()
            usuario_teste, criado = User.objects.get_or_create(
                username='vendedor_teste',
                defaults={'email': 'vendedor@teste.com'}
            )

            
            for form in formset:
                if form.has_changed():
                    anuncio = form.save(commit=False)
                    anuncio.festa = festa
                    

                    anuncio.pessoal = usuario_teste 
                    
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
    
    anuncios = Anuncio.objects.filter(festa=festa)
    
    context = {
        'festa': festa,
        'anuncios': anuncios
    }

    return render(request, 'ingressos/catalogo_ingressos.html', context)