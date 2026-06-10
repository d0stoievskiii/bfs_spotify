from typing import List, Optional, Set
from collections import deque
from spotify_integration.client import get_similar_artists

def obter_vizinhos_lastfm(nome_artista: str) -> List[str]:
    try:
        dados = get_similar_artists(nome_artista, limit=30)
        return [artista["name"] for artista in dados]
    except Exception as e:
        print(f"Erro na API Last.fm para {nome_artista}: {e}")
        return []

def bfs_via_api(artista_origem: str, artista_destino: str, max_depth: int = 3) -> Optional[List[str]]:

    if artista_origem.lower() == artista_destino.lower():
        return [artista_origem]

    fila = deque([(artista_origem, [artista_origem])])
    visitados: Set[str] = {artista_origem.lower()}

    while fila:
        artista_atual, caminho_atual = fila.popleft()
      
        if len(caminho_atual) > max_depth:
            continue

        vizinhos = obter_vizinhos_lastfm(artista_atual)

        for vizinho in vizinhos:
            vizinho_lower = vizinho.lower()
            
            if vizinho_lower not in visitados:
                novo_caminho = caminho_atual + [vizinho]

                if vizinho_lower == artista_destino.lower():
                    return novo_caminho

                visitados.add(vizinho_lower)
                fila.append((vizinho, novo_caminho))

    return None
