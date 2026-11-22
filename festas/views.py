from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Festa
from .forms import FestaForm
import calendar
from datetime import date



def feed_festas(request):
    festas_cadastradas = Festa.objects.all().order_by('data_festa')

    hoje = date.today()
    ano, mes = hoje.year, hoje.month

    festas_mes = festas_cadastradas.filter(data_festa__year=ano, data_festa__month=mes)
    festas_por_dia = {}
    for festa in festas_mes:
        dia = festa.data_festa.day
        festas_por_dia.setdefault(dia, []).append(festa)

   
    cal = calendar.Calendar(firstweekday=6)
    semanas = []
    for semana in cal.monthdayscalendar(ano, mes):
        linha = []
        for dia in semana:
            linha.append({
                'dia': dia,
                'festas': festas_por_dia.get(dia, [])
            })
        semanas.append(linha)

    return render(request, 'festas/feed.html', {
        'festas': festas_cadastradas,
        'semanas': semanas,
        'mes_ano': hoje.strftime('%m/%Y'),
    })

@login_required(login_url='login')
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

