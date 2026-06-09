from django.http import JsonResponse
import logging

from webapp.services.orchestrator import buscar_conexao_inteligente
from webapp.services.formatters import formatar_caminho_para_arvore
from spotify_integration.client import get_token, search_for_artist

logger = logging.getLogger(__name__)

def buscar_conexao_view(request):
    origem = request.GET.get('origem')
    destino = request.GET.get('destino')

    if not origem or not destino:
        return JsonResponse({"erro": "Parâmetros 'origem' e 'destino' obrigatórios."}, status=400)

    caminho = buscar_conexao_inteligente(origem, destino)

    if not caminho:
        return JsonResponse(
            {"erro": "Nenhuma conexão encontrada nas bases de dados."},
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
        logger.warning(f"Aviso: Falha ao carregar imagens do Spotify: {e}")

    arvore_json = formatar_caminho_para_arvore(caminho, cache_imagens_final)
    return JsonResponse(arvore_json, json_dumps_params={'ensure_ascii': False})
