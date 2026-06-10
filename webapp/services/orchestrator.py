import logging
from typing import List, Optional
from spotify_data.collab_search import bfs as duckdb_bfs, get_artist_rowid_by_name
from webapp.services.bfs_lastfm import bfs_via_api

logger = logging.getLogger(__name__)

def buscar_conexao_inteligente(origem: str, destino: str) -> Optional[List[str]]:

    try:
        id_origem = int(get_artist_rowid_by_name(origem))
        id_destino = int(get_artist_rowid_by_name(destino))
        caminho_duckdb = duckdb_bfs(id_origem, id_destino)
        
        if caminho_duckdb:
            logger.info(f"Conexão encontrada via DuckDB: {origem} -> {destino}")
            return caminho_duckdb
            
    except Exception as e:
        logger.warning(f"DuckDB falhou para {origem} e {destino}. Erro: {e}")

    logger.info(f"Iniciando Fallback Last.fm para: {origem} -> {destino}")
    
    try:
        caminho_lastfm = bfs_via_api(origem, destino, max_depth=3)
        
        if caminho_lastfm:
            logger.info("Conexão encontrada via Last.fm API!")
            return caminho_lastfm
            
    except Exception as e:
        logger.error(f"Last.fm também falhou: {e}")

    return None
