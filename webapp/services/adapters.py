from typing import List
from spotify_integration.client import get_similar_artists
from spotify_data.collab_search import *

def adaptador_api_para_bfs(nome_do_artista: str) -> List[str]:

    print(f"   [Sistema] Buscando conexões para: {nome_do_artista}...")
    try:
        dados = get_similar_artists(nome_do_artista, limit=10)
        return [artista["name"] for artista in dados]
    except Exception as e:
        print(f"   [ERRO] Falha ao buscar {nome_do_artista}: {e}")
        return []
    
def adaptador_collabs_spotify_data(nome_do_artista: str) -> list[str]:

    print(f"   [Sistema] Buscando conexões para: {nome_do_artista}...")
    try:
        artist_rowid = get_artist_rowid_by_name(nome_do_artista)
        rows = con.execute(f"""
            SELECT source_id, target_id
            FROM artist_edges
            WHERE source_id = {artist_rowid}
        """).fetchall()
        return [get_artist_name_by_rowid(int(r[1]))["name"][0] for r in rows]
    except Exception as e:
        print(f"   [ERRO] Falha ao buscar {nome_do_artista}: {e}")
        return []
