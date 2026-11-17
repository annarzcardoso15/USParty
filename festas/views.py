from django.shortcuts import render, redirect, get_object_or_404
from .models import Festa 
from .forms import FestaForm

def feed_festas(request):

    festas_cadastradas = Festa.objects.all()
    contexto = {
        'festas': festas_cadastradas
    }
    
    return render(request, 'festas/feed.html', contexto)

def criar_festa(request):
    if request.method == 'POST':
        form = FestaForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('feed_festas')
    else:
        form = FestaForm()

    return render(request, 'festas/criar_festa.html', {'form': form})

def detalhes_festa(request, idfesta):
    
    festa_especifica = get_object_or_404(Festa, pk=idfesta)
    
    return render(request, 'festas/detalhes_festa.html', {'festa': festa_especifica})