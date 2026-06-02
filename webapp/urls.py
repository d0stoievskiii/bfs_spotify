from django.urls import path
from .views import buscar_conexao_view

urlpatterns = [
    path('buscar', buscar_conexao_view, name='buscar_conexao'),
]