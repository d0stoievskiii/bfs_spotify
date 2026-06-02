from typing import List, Callable, Optional, Set

class NoPathFoundError(Exception):
    pass

def encontrar_conexao_artistas(
        artista_origem: str,
        artista_destino: str,
        funcao_buscar_vizinhos: Callable[[str], List[str]],
        grau_maximo: int = 4
) -> Optional[List[str]]:

    if artista_origem == artista_destino:
        return [artista_origem]

    fila: List[tuple[str, List[str]]] = [(artista_origem, [artista_origem])]
    visitados: Set[str] = {artista_origem}

    while fila:
        artista_atual, caminho_atual = fila.pop(0)

        if len(caminho_atual) > grau_maximo:
            continue

        vizinhos = funcao_buscar_vizinhos(artista_atual)

        for vizinho in vizinhos:
            if vizinho not in visitados:
                novo_caminho = caminho_atual + [vizinho]

                if vizinho == artista_destino:
                    return novo_caminho

                visitados.add(vizinho)
                fila.append((vizinho, novo_caminho))

    return None