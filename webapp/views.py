from django.http import JsonResponse
from .services.bfs import encontrar_conexao_artistas
from .services.adapters import adaptador_api_para_bfs
from .services.formatters import formatar_caminho_para_arvore


def buscar_conexao_view(request):

    origem = request.GET.get('origem')
    destino = request.GET.get('destino')

    if not origem or not destino:
        return JsonResponse(
            {"erro": "Os parâmetros 'origem' e 'destino' são obrigatórios."},
            status=400
        )

    caminho = encontrar_conexao_artistas(
        artista_origem=origem,
        artista_destino=destino,
        funcao_buscar_vizinhos=adaptador_api_para_bfs,
        grau_maximo=3
    )

    if not caminho:
        return JsonResponse(
            {"erro": "Nenhuma conexão encontrada no grau máximo estipulado."},
            status=404
        )

    arvore_json = formatar_caminho_para_arvore(caminho)

    return JsonResponse(arvore_json, json_dumps_params={'ensure_ascii': False})