from django.urls import path
from .views import buscar_conexao_view, artist_autocomplete

urlpatterns = [
    path('buscar', buscar_conexao_view, name='buscar_conexao'),
    path("artists/autocomplete/", artist_autocomplete, name="artist_autocomplete"),
]