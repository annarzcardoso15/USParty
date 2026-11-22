from django.urls import path
from . import views

urlpatterns = [
    path('anunciar', views.criar_etapa1, name='criar_etapa1'),
    path('detalhes-ingresso', views.criar_etapa2, name='criar_etapa2'),
    path('catalogo/<int:festa_id>/', views.catalogo_ingressos, name='catalogo_ingressos'),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
    path('anuncio/<int:id_anuncio>/editar/', views.editar_anuncio, name='editar_anuncio'),
    path('anuncio/<int:id_anuncio>/excluir/', views.excluir_anuncio, name='excluir_anuncio'),
]