import duckdb
from collections import deque

try:
    con = duckdb.connect("spotify_data/data/spotify_graph.duckdb", read_only=True)
except Exception as e:
    con = None
    print(f"Aviso: Banco DuckDB não encontrado. O sistema irá usar o fallback do Last.fm. Erro: {e}")

def get_artist_name_by_rowid(artist_rowid):
    s = con.execute(f"""
        SELECT name
        FROM artists
        WHERE id = {artist_rowid}
        """).df()
    if (len(s.index) == 0):
        raise Exception(f"Nenhum artista encontrado com id {artist_rowid}")
    return s

def get_artist_rowid_by_name(artist_name):
    s = con.execute("""
        SELECT id, popularity
        FROM artists
        WHERE name_normalized = ?
        """,[str(artist_name).strip().lower()]).df()
    if (len(s.index) == 0):
        raise Exception(f"Nenhum artista encontrado com nome {artist_name}")
    if (len(s.index) > 1):
        return s.sort_values(by="popularity", ascending=False)["id"][0]
    else:
        return s["id"][0]

def expand_frontier(frontier, visited):
    rows = con.execute("""
        SELECT source_id, target_id
        FROM artist_edges
        WHERE source_id = ANY(?)
          AND NOT (target_id = ANY(?))
    """, [list(frontier), list(visited)]).fetchall()

    return rows

def expand_frontier_by_name(artist_name: str) -> list[str]:
    artist_rowid = get_artist_rowid_by_name(artist_name)
    rows = con.execute(f"""
        SELECT source_id, target_id
        FROM artist_edges
        WHERE source_id = {artist_rowid}
    """).fetchall()

    return [get_artist_name_by_rowid(int(r[1]))["name"][0] for r in rows]


def bfs(start_id, target_id, max_depth=10):
    visited = {start_id}
    frontier = {start_id}
    parent = {start_id: None}

    for depth in range(max_depth):
        rows = expand_frontier(frontier, visited)

        next_frontier = set()

        for source, target in rows:
            if target in visited:
                continue

            visited.add(target)
            parent[target] = source
            next_frontier.add(target)

            if target == target_id:
                return reconstruct_path(parent, start_id, target_id)

        frontier = next_frontier

        if not frontier:
            break

    return None


def reconstruct_path(parent, start_id, target_id):
    path = []
    current = target_id

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    if path[0] != start_id:
        return None

    return [get_artist_name_by_rowid(int(p))["name"][0] for p in path]
    

