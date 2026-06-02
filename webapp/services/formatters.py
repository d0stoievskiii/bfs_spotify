from typing import List, Dict, Any

def formatar_caminho_para_arvore(caminho: List[str]) -> Dict[str, Any]:
    
    if not caminho:
        return {}

    no_atual: Dict[str, Any] = {
        "nome": caminho[-1],
        "filhos": []
    }

    for artista in reversed(caminho[:-1]):
        no_atual = {
            "nome": artista,
            "filhos": [no_atual]
        }

    return no_atual