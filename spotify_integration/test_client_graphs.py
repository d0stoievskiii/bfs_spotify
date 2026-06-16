import sys
import os

# Adiciona diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from collections import deque
from spotify_data.collab_search import (
    get_artist_rowid_by_name,
    get_artist_name_by_rowid,
    expand_frontier,
    con
)

def explore_artist_network(artist_name: str, max_depth: int = 6):
    if con is None:
        raise Exception("Banco de dados DuckDB não disponível!")
    
    try:
        start_id = int(get_artist_rowid_by_name(artist_name))
        print(f"Artista inicial: {artist_name} (ID: {start_id})")
    except Exception as e:
        print(f"Erro ao encontrar artista: {e}")
        return None
    
    visited = {start_id}
    frontier = {start_id}
    levels_data = []
    
    # Level 0: Starting artist
    levels_data.append({
        'level': 0,
        'frontier_size': 1,
        'cumulative_artists': 1
    })
    
    print(f"\nExpansão da Rede para '{artist_name}':")
    print(f"Nível 0: 1 artista (ponto de partida)")
    
    # Explore successive levels
    for depth in range(1, max_depth + 1):
        # Convert sets to lists with proper integer conversion
        frontier_list = [int(x) for x in frontier]
        visited_list = [int(x) for x in visited]
        rows = expand_frontier(set(frontier_list), set(visited_list))
        
        if not rows:
            print(f"Nível {depth}: Nenhum novo artista encontrado. Rede esgotada.")
            break
        
        next_frontier = set()
        for source, target in rows:
            if target not in visited:
                visited.add(target)
                next_frontier.add(target)
        
        frontier = next_frontier
        
        levels_data.append({
            'level': depth,
            'frontier_size': len(frontier),
            'cumulative_artists': len(visited)
        })
        
        print(f"Nível {depth}: {len(frontier)} novos artistas encontrados | Total: {len(visited)} artistas")
    
    return levels_data

def plot_network_expansion(levels_data: list, artist_name: str):
    if not levels_data:
        return
    
    levels = [d['level'] for d in levels_data]
    frontier_sizes = [d['frontier_size'] for d in levels_data]
    cumulative = [d['cumulative_artists'] for d in levels_data]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Frontier size per level (new artists discovered)
    ax1.bar(levels, frontier_sizes, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Nível da Rede', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Novos Artistas Encontrados', fontsize=11, fontweight='bold')
    ax1.set_title(f"Expansão da Rede - '{artist_name}'\n(Artistas encontrados em cada nível)", 
                  fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_xticks(levels)
    
    # Add extra top margin for bar labels
    max_bar = max(frontier_sizes)
    ax1.set_ylim(0, max_bar * 1.15)
    
    # Add value labels on bars
    for level, size in zip(levels, frontier_sizes):
        ax1.text(level, size + max_bar*0.02, str(size), 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Plot 2: Cumulative artists discovered
    ax2.plot(levels, cumulative, marker='o', linewidth=2.5, markersize=8, 
            color='darkgreen', label='Artistas Acumulados')
    ax2.fill_between(levels, cumulative, alpha=0.3, color='green')
    ax2.set_xlabel('Nível da Rede', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Artistas Acumulados', fontsize=11, fontweight='bold')
    ax2.set_title(f"Crescimento do Tamanho Total da Rede\n(Colaboradores acumulados)", 
                  fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.set_xticks(levels)
    
    # Add extra top margin for point labels
    max_cumulative = max(cumulative)
    ax2.set_ylim(0, max_cumulative * 1.15)
    
    # Add value labels on points
    for level, total in zip(levels, cumulative):
        ax2.text(level, total + max_cumulative*0.02, str(total), 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('network_expansion.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico salvo como 'network_expansion.png'")
    plt.show()

if __name__ == "__main__":
    artist = "MOZART"
    
    print("=" * 60)
    print(f"Análise de Rede de Colaboração DuckDB")
    print("=" * 60)
    
    # Explore the network
    network_data = explore_artist_network(artist, max_depth=20)
    
    if network_data:
        print("\n" + "=" * 60)
        print("Resumo:")
        print(f"  Total de artistas na rede: {network_data[-1]['cumulative_artists']}")
        print(f"  Profundidade máxima explorada: {network_data[-1]['level']}")
        print(f"  Taxa de expansão da rede: {network_data[-1]['frontier_size']:.0f} novos artistas no nível final")
        print("=" * 60)
        
        # Create visualization
        plot_network_expansion(network_data, artist)
