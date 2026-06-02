from django.urls import path
from .views import buscar_conexao_view

urlpatterns = [
    # Mapeia a URL /buscar para a função buscar_conexao_view
    path('buscar', buscar_conexao_view, name='buscar_conexao'),
]