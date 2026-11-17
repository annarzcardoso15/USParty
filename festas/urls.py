from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_festas, name='feed_festas'),
]