from django.urls import path
from . import views

urlpatterns = [
    path('interesse/<int:anuncio_id>/', views.manifestar_interesse, name='manifestar_interesse'),
]