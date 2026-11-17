from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_festas, name='feed_festas'),
    path('criar/', views.criar_festa, name='criar_festa'),
    path('<int:idfesta>/', views.detalhes_festa, name='detalhes_festa'),
]