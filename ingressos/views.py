# Criar página de criar anuncios, vitrine dos ingressos e meus anuncios.
from django.shortcuts import render, redirect, HttpResponse
from django.forms import modelformset_factory
from .models import Anuncio
from .forms import Etapa1Form, Etapa2Form

def criar_etapa1(request):
    if request.method == 'POST':
        form = Etapa1Form(request.POST)
        if form.is_valid():
            request.session['festa_id'] = form.cleaned_data['festa'].id
            request.session['quantidade'] = form.cleaned_data['quantidade']
            

            return redirect('criar_etapa2') 
    else:
        form = Etapa1Form()
        
    return render(request, 'ingressos/etapa1.html', {'form': form})

def criar_etapa2(request):
    quantidade = request.session.get('quantidade', 1)
    festa_id = request.session.get('festa_id')


    IngressoFormSet = modelformset_factory(Anuncio, form=Etapa2Form, extra=quantidade)

    if request.method == 'POST':
        formset = IngressoFormSet(request.POST, queryset=Anuncio.objects.none())
        
        if formset.is_valid():
            ingressos = formset.save(commit=False)
            

            for ingresso in ingressos:
                ingresso.festa_id = festa_id 
                ingresso.save() 
                

            if 'quantidade' in request.session:
                del request.session['quantidade']
                del request.session['festa_id']
                
            return HttpResponse("<h1 style='text-align: center; color: #247BA0; margin-top: 50px;'>Ingressos criados com sucesso! 🎉</h1><p style='text-align: center;'><a href='/ingressos/criar/passo1/'>Criar mais anúncios</a></p>")
    else:
        formset = IngressoFormSet(queryset=Anuncio.objects.none())

    return render(request, 'ingressos/etapa2.html', {'formset': formset})