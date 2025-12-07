import matplotlib.pyplot as plt
import numpy as np

# Configuração de Cores para os pares
COLORS = {0: 'white', 1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'purple', 6: 'cyan'}

def draw_grid_live(game, delay=0.01):
    """
    Desenha o estado atual do grid em tempo real.
    """
    if not hasattr(draw_grid_live, 'fig'):
        plt.ion() # Modo interativo
        draw_grid_live.fig, draw_grid_live.ax = plt.subplots(figsize=(5,5))
    
    ax = draw_grid_live.ax
    ax.clear()
    
    nrows, ncols = game.qtd_linhas, game.qtd_colunas
    
    # Desenha o grid
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_xticks(np.arange(ncols+1))
    ax.set_yticks(np.arange(nrows+1))
    ax.grid(True, color='black')
    ax.invert_yaxis() # (0,0) no topo esquerdo
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Pinta as células
    for r in range(nrows):
        for c in range(ncols):
            val = game.grid[r][c]
            if val != 0:
                color = COLORS.get(val, 'gray')
                rect = plt.Rectangle((c, r), 1, 1, facecolor=color)
                ax.add_patch(rect)
                ax.text(c+0.5, r+0.5, str(val), ha='center', va='center', 
                        color='white', fontweight='bold')
            elif (r, c) in getattr(game, 'endpoints', []):
                 # Marca endpoints vazios se necessário
                 pass

    plt.draw()
    plt.pause(delay)