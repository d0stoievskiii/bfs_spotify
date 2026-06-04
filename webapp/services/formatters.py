from typing import List, Dict, Any

def formatar_caminho_para_arvore(caminho: List[str], cache_imagens: Dict[str, str]) -> Dict[str, Any]:
    
    if not caminho:
        return {}

    img_padrao = "https://i.scdn.co/image/ab6761610000e5eb55d39ab9c21d506aa52f7021"

    no_atual: Dict[str, Any] = {
        "nome": caminho[-1],
        "imagem": cache_imagens.get(caminho[-1].strip().lower(), img_padrao),
        "filhos": []
    }

    for artista in reversed(caminho[:-1]):
        no_atual = {
            "nome": artista,
            "imagem": cache_imagens.get(artista.strip().lower(), img_padrao),
            "filhos": [no_atual]
        }

    return no_atual