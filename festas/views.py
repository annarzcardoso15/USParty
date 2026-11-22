from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Festa
from .forms import FestaForm

def feed_festas(request):

    festas_cadastradas = Festa.objects.all()
    contexto = {
        'festas': festas_cadastradas
    }
    
    return render(request, 'festas/feed.html', contexto)

@login_required
def criar_festa(request):
    is_adm = hasattr(request.user, 'adm')
    is_instituicao = hasattr(request.user, 'instituicao')

    if not (is_adm or is_instituicao):
        return HttpResponseForbidden("Apenas administradores ou instituições podem criar festas.")

    if request.method == 'POST':
        form = FestaForm(request.POST)
        if form.is_valid():
            nova_festa = form.save(commit=False)

            if is_adm:
                nova_festa.adm = request.user.adm

            nova_festa.save()
            form.save_m2m()

            if is_instituicao:
                nova_festa.organizadores.add(request.user.instituicao)

            return redirect('feed_festas')
    else:
        form = FestaForm()

    return render(request, 'festas/criar_festa.html', {'form': form})

def detalhes_festa(request, idfesta):
    
    festa_especifica = get_object_or_404(Festa, pk=idfesta)
    
    return render(request, 'festas/detalhes_festa.html', {'festa': festa_especifica})