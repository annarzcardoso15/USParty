from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),

    # Recuperação de senha (views prontas do Django)
    path('senha/esqueci/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/senha_esqueci.html',
        email_template_name='usuarios/senha_email.txt',
    ), name='password_reset'),
    path('senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/senha_enviado.html',
    ), name='password_reset_done'),
    path('senha/nova/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/senha_nova.html',
    ), name='password_reset_confirm'),
    path('senha/pronto/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/senha_pronto.html',
    ), name='password_reset_complete'),
]