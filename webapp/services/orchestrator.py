import logging
from typing import List, Optional
from spotify_data.collab_search import bfs as duckdb_bfs, get_artist_rowid_by_name
from webapp.services.bfs_lastfm import bfs_via_api
from spotify_integration.client import search_for_artist, get_token, search_for_artist_unsafe

logger = logging.getLogger(__name__)

def buscar_conexao_inteligente(origem, destino) -> Optional[List[str]]:
    try:
        rowid_origem = get_artist_rowid_by_name(origem)
        rowid_destino = get_artist_rowid_by_name(destino)

        if rowid_origem is not None and rowid_destino is not None:

            caminho_duckdb = duckdb_bfs(
                int(rowid_origem),
                int(rowid_destino)
            )

            if caminho_duckdb:

                logger.info(
                    f"Conexão encontrada via DuckDB: {origem} -> {destino}"
                )

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
