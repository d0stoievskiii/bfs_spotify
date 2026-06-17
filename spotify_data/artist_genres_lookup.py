import duckdb

try:
    con = duckdb.connect("spotify_data/data/artist_genres.duckdb", read_only=True)
except Exception as e:
    con = None
    print(f"Aviso: Banco DuckDB não encontrado. Erro: {e}")


def get_genres_by_artist_rowid(artist_rowid):
    s = con.execute("""
        SELECT genre
        FROM artist_genres
        WHERE artist_rowid = ?
        """, [artist_rowid]).df()
    if len(s.index) == 0:
        raise Exception(f"Nenhum gênero encontrado para artist_rowid {artist_rowid}")
    return s["genre"].tolist()


def get_artist_rowids_by_genre(genre):
    s = con.execute("""
        SELECT artist_rowid
        FROM artist_genres
        WHERE genre = ?
        """, [str(genre).strip().lower()]).df()
    if len(s.index) == 0:
        raise Exception(f"Nenhum artista encontrado com gênero {genre}")
    return s["artist_rowid"].tolist()


def artist_has_genre(artist_rowid, genre):
    s = con.execute("""
        SELECT 1
        FROM artist_genres
        WHERE artist_rowid = ? AND genre = ?
        """, [artist_rowid, str(genre).strip().lower()]).df()
    return len(s.index) > 0


def shared_genres(artist_rowid_a, artist_rowid_b):
    s = con.execute("""
        SELECT a.genre
        FROM artist_genres a
        JOIN artist_genres b
          ON a.genre = b.genre
        WHERE a.artist_rowid = ? AND b.artist_rowid = ?
        """, [artist_rowid_a, artist_rowid_b]).df()
    return s["genre"].tolist()
