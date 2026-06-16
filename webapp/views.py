import logging
import concurrent.futures
from django.http import JsonResponse
from django.shortcuts import render

from .services.orchestrator import buscar_conexao_inteligente
from .services.formatters import formatar_caminho_para_arvore
from webapp.models import Artist
from spotify_integration.client import get_token, search_for_artist

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def buscar_conexao_view(request):

    origem = request.GET.get('origem')
    destino = request.GET.get('destino')

    if not origem or not destino:
        return JsonResponse({"erro": "Parâmetros 'origem' e 'destino' obrigatórios."}, status=400)

    caminho = buscar_conexao_inteligente(origem, destino)

    if not caminho:
        return JsonResponse({"erro": "Nenhuma conexão encontrada nas bases de dados."}, status=404)

    cache_imagens_final = {}
    try:
        token = get_token()

        def buscar_imagem_individual(nome_artista):
            dados = search_for_artist(token, nome_artista)
            if dados and dados.get("images"):
                return nome_artista, dados["images"][0]["url"]
            return nome_artista, None

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            resultados = executor.map(buscar_imagem_individual, caminho)

        for nome, url in resultados:
            if url:
                cache_imagens_final[nome.strip().lower()] = url

    except Exception as e:
        logger.warning(f"Aviso: Falha ao carregar imagens do Spotify: {e}")

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