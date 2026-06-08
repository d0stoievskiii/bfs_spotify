from django.http import JsonResponse
from django.db.models import Case, When, IntegerField
from .services.bfs import encontrar_conexao_artistas
from .services.adapters import adaptador_api_para_bfs
from .services.formatters import formatar_caminho_para_arvore
from spotify_integration.client import get_token, search_for_artist
from django.shortcuts import render

from spotify_data.collab_search import *
from .models import Artist

def index(request):
    return render(request, 'index.html')

def buscar_conexao_view(request):

    origem = request.GET.get('origem')
    destino = request.GET.get('destino')

    if not origem or not destino:
        return JsonResponse(
            {"erro": "Os parâmetros 'origem' e 'destino' são obrigatórios."},
            status=400
        )

    caminho = bfs(int(get_artist_rowid_by_name(origem)), int(get_artist_rowid_by_name(destino)))

    if not caminho:
        return JsonResponse(
            {"erro": "Nenhuma conexão encontrada no grau máximo estipulado."},
            status=404
        )
    
    cache_imagens_final = {}
    try:
        token = get_token()
        for nome_artista in caminho:
            dados_spotify = search_for_artist(token, nome_artista)
            
            if dados_spotify and dados_spotify.get("images"):
                chave_limpa = nome_artista.strip().lower()
                cache_imagens_final[chave_limpa] = dados_spotify["images"][0]["url"]
    except Exception as e:
        print(f"Aviso: Não foi possível carregar as imagens do Spotify: {e}")

    arvore_json = formatar_caminho_para_arvore(caminho, cache_imagens_final)

    return JsonResponse(arvore_json, json_dumps_params={'ensure_ascii': False})


def normalize_query(value: str) -> str:
    return value.strip().lower()


def artist_autocomplete(request):
    query = normalize_query(request.GET.get("q", ""))

    if len(query) < 2:
        return JsonResponse({"results": []})

    artists = (
        Artist.objects
        .filter(name_normalized__startswith=query)
        .order_by("-popularity", "-followers_total", "name")
        .values("id", "name", "popularity", "followers_total")[:20]
    )

    return JsonResponse({"results": list(artists)})


