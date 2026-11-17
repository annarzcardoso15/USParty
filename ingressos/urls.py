from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_anuncio, name='criar_anuncio'),
    path('vitrine/<int:festa_id>/', views.vitrine_ingressos, name='vitrine_ingressos'),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
]