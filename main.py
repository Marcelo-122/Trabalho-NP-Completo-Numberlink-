from game import NumberLink
from visualizer import draw_grid_live
import sys
import time
import random

# Aumenta limite para suportar a profundidade da recursão em grids complexos
sys.setrecursionlimit(50000)

class Automato:
    """
    Solver que utiliza Backtracking com poda via BFS e ordenação heurística.
    """
    def __init__(self, game: NumberLink, pq_pares: list[int]):
        self.game = game
        self.pq_pares = pq_pares
        self.passos = 0
        self.start_time = time.time()
        self.sucesso = False # Flag para indicar se resolveu
        
        primeiro_id = pq_pares[0]
        pos_inicial = self.game.pares[primeiro_id][0]
        
        # Tenta resolver. Se retornar True, marca sucesso.
        if self.solve(0, pos_inicial):
            self.sucesso = True
            tempo = time.time() - self.start_time
            print(f"\n✅ Solução encontrada em {tempo:.2f}s e {self.passos} passos!")
            self.game.display()
        else:
            print(f"\n❌ Falha após {self.passos} passos.")

    def solve(self, par_index, pos_atual):
        # draw_grid_live(self.game.grid, delay=0.01)  # Visualização ao vivo, caso queria só descomente.
        """Recursão principal (Backtracking)."""
        self.passos += 1
        
        # Caso Base: Todos os pares resolvidos
        if par_index >= len(self.pq_pares):
            return True

        par_id = self.pq_pares[par_index]
        destino = self.game.pares[par_id][1]

        # 1. Verificação de Chegada
        # Se alcançou o destino, encerra este par e inicia o próximo imediatamente.
        if pos_atual == destino:
            if par_index + 1 < len(self.pq_pares):
                prox_id = self.pq_pares[par_index + 1]
                prox_inicio = self.game.pares[prox_id][0]
                return self.solve(par_index + 1, prox_inicio)
            else:
                return True # Sucesso Total

        # 2. Definição de Movimentos
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Heurística: Tenta ir na direção do alvo primeiro (A*)
        movimentos.sort(key=lambda m: abs((pos_atual[0]+m[0]) - destino[0]) + abs((pos_atual[1]+m[1]) - destino[1]))

        l, c = pos_atual
        
        for dl, dc in movimentos:
            nl, nc = l + dl, c + dc
            
            if not self.game.is_valid_move(nl, nc):
                continue
            
            val_vizinho = self.game.grid[nl][nc]
            eh_destino = ((nl, nc) == destino)

            # Só move se for vazio ou se for o destino final
            if val_vizinho == 0 or eh_destino:
                if eh_destino:
                    # Avança sem modificar o grid (destino é fixo)
                    if self.solve(par_index, (nl, nc)): return True
                else:
                    # Aplica movimento (pinta célula)
                    self.game.grid[nl][nc] = par_id
                    
                    # Poda: Verifica se o movimento quebrou a conectividade de outros pares
                    if self.game.check_connectivity(par_id):
                        if self.solve(par_index, (nl, nc)):
                            return True
                    
                    # Backtrack: Desfaz movimento se falhou
                    self.game.grid[nl][nc] = 0
        
        return False

# --- Execução Principal ---
if __name__ == "__main__":
    print("\n=== Puzzle NumberLink 8x8 ==")
    
    pares_8x8 = {
        1: [(0, 0), (4, 4)], # Diagonal longa
        2: [(0, 7), (3, 3)], # Diagonal oposta parcial
        3: [(7, 0), (5, 2)], # Canto inferior esquerdo
        4: [(7, 7), (5, 5)], # Canto inferior direito
        5: [(2, 0), (6, 3)], # Meio esquerda -> baixo
        6: [(1, 7), (4, 5)], # Meio direita -> centro
    }
    # Configuração Inicial
    game_ref = NumberLink(8, 8, pares_8x8)
    lista_ids = list(game_ref.pares.keys())

    # Heurística Inicial: Tenta resolver os caminhos mais longos primeiro
    # (Calcula Distância Manhattan entre Início e Fim de cada par)
    lista_ids.sort(key=lambda pid: abs(game_ref.pares[pid][0][0] - game_ref.pares[pid][1][0]) + 
                                   abs(game_ref.pares[pid][0][1] - game_ref.pares[pid][1][1]), reverse=True)

    MAX_TENTATIVAS = 100
    
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        print(f"\n--- Tentativa #{tentativa} | Ordem: {lista_ids} ---")
        
        # Cria uma cópia limpa do jogo para esta tentativa
        game_copia = NumberLink(8, 8, pares_8x8)
        automato = Automato(game_copia, lista_ids)
        
        if automato.sucesso:
            break
        
        print("Falha. Tentando nova permutação aleatória...")
        random.shuffle(lista_ids) # Random Restart
    else:
        print("\nNão foi possível encontrar solução após todas as tentativas.")