from typing import List
from spotify_integration.client import get_similar_artists

def adaptador_api_para_bfs(nome_do_artista: str) -> List[str]:

    print(f"   [Sistema] Buscando conexões para: {nome_do_artista}...")
    try:
        dados = get_similar_artists(nome_do_artista, limit=10)
        return [artista["name"] for artista in dados]
    except Exception as e:
        print(f"   [ERRO] Falha ao buscar {nome_do_artista}: {e}")
        return []