from django.shortcuts import render
from .models import Festa 

def feed_festas(request):

    festas_cadastradas = Festa.objects.all()
    contexto = {
        'festas': festas_cadastradas
    }
    
    return render(request, 'festas/feed.html', contexto)