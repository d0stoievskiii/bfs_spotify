## spotify_data

* baixe o arquivo spotify_graph.duckdb (https://drive.google.com/drive/folders/1X2t9K7DetoDrn0zyqz5Nun3eYMyAG4BS?usp=sharing)
* coloque em spotify_data/data/
* spotify_data.collab_search vem com uma implementação do bfs, mas pode-se usar expand_frontier em outra implementação também
* não esquece da instalar as novas dependencias! ative o environment e pip install -r requirements.txt

Exemplo de uso:

```
from spotify_data.collab_search import *
bfs(int(get_artist_rowid_by_name("Jay-Z")), int(get_artist_rowid_by_name("Tim Maia")))
```

```output
['JAY-Z', 'Jeymes Samuel', 'Jorge Ben Jor', 'Tim Maia']
```

