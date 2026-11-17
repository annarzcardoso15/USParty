# Criar página de criar anuncios, vitrine dos ingressos e meus anuncios.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AnuncioForm


#@login_required
def criar_anuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.vendedor = request.user.pessoal 
            anuncio.status = "Disponível"
            
            anuncio.save() 
            

            return redirect('meus_anuncios') #talvez redirecionar pra pagina com a vitrine de ingressos 
    else:
        form = AnuncioForm()

    return render(request, 'ingressos/criar_anuncio.html', {'form': form})

def vitrine_ingressos(request, festa_id):
    #Colocar a logica da vitrine do site 
    pass

def meus_anuncios(request, festa_id):
    #Colocar a logica da vitrine do site 
    pass