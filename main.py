from game import NumberLink
from priorityQueue import PriorityQueue, Node
from visualizer import draw_grid_live
import sys
import time

# Aumenta o limite de recursão para permitir caminhos longos em grids complexos
sys.setrecursionlimit(20000)

class Automato:
    """
    Agente solucionador que utiliza Busca em Profundidade (DFS) com Backtracking
    e poda baseada em heurística de isolamento.
    """
    def __init__(self, game: NumberLink, pq_pares: list[int]):
        self.game = game
        self.pq_pares = pq_pares # Lista ordenada de prioridade dos pares a resolver
        self.passos = 0
        self.start_time = time.time()
        
        # Inicia a recursão a partir do primeiro par da lista
        primeiro_par = pq_pares[0]
        pos_inicial = self.game.pares[primeiro_par][0]
        
        print(f"Iniciando resolução...")
        
        if self.solve(0, pos_inicial):
            tempo = time.time() - self.start_time
            print(f"\n✅ Solução encontrada em {tempo:.4f}s e {self.passos} passos!")
            self.game.display()
        else:
            print("\n❌ Não foi possível encontrar solução.")

    def check_isolation(self, active_par_id):
        """
        HEURÍSTICA DE PODA (PRUNING):
        Verifica se o movimento atual bloqueou acidentalmente o início ou fim 
        de qualquer outro par que ainda não foi conectado.
        
        Retorna:
            True: Se detectou que algum par ficou isolado (sem saída).
            False: Se o grid continua viável.
        """
        for pid in self.pq_pares:
            # Ignora o par que está sendo movido no momento
            if pid == active_par_id: continue
            
            p1, p2 = self.game.pares[pid]
            
            # Verifica quantos vizinhos livres restam nos endpoints deste par
            n1 = self.game.count_free_neighbors(p1[0], p1[1])
            n2 = self.game.count_free_neighbors(p2[0], p2[1])
            
            # Se algum endpoint ficou com 0 vizinhos livres, o caminho está bloqueado
            if n1 == 0 or n2 == 0:
                return True 
        return False

    def solve(self, par_index, pos_atual):
        """
        Algoritmo Recursivo Principal (Backtracking).
        Tenta preencher o caminho para o par atual e, se sucesso, chama a si mesmo para o próximo.
        """
        draw_grid_live(self.game, delay=0.001)
        self.passos += 1
        
        # Caso Base: Se o índice ultrapassou a lista, todos os pares foram resolvidos.
        if par_index >= len(self.pq_pares):
            return True

        par_id = self.pq_pares[par_index]
        destino = self.game.pares[par_id][1]

        # 1. Verifica se alcançou o destino do par atual
        if pos_atual == destino:
            # Se existem mais pares, inicia a busca para o próximo (par_index + 1)
            if par_index + 1 < len(self.pq_pares):
                prox_id = self.pq_pares[par_index + 1]
                prox_inicio = self.game.pares[prox_id][0]
                return self.solve(par_index + 1, prox_inicio)
            else:
                return True # Todos os pares conectados com sucesso

        # 2. Define movimentos possíveis: (delta_linha, delta_coluna)
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # HEURÍSTICA DE ORDENAÇÃO:
        # Ordena os movimentos pela distância Manhattan até o destino.
        # Tenta ir na direção do objetivo primeiro, mas permite desvios se necessário.
        movimentos.sort(key=lambda m: abs((pos_atual[0]+m[0]) - destino[0]) + abs((pos_atual[1]+m[1]) - destino[1]))

        l, c = pos_atual
        
        for dl, dc in movimentos:
            nl, nc = l + dl, c + dc
            
            # Verifica se a célula alvo é válida (vazia ou destino)
            if self.game.is_valid_move(nl, nc, par_id):
                
                eh_destino = ((nl, nc) == destino)
                
                if eh_destino:
                    # Se chegou no destino, avança a recursão sem pintar a célula (já tem o ID)
                    if self.solve(par_index, (nl, nc)): return True
                else:
                    # --- APLICA MOVIMENTO (In-Place) ---
                    self.game.grid[nl][nc] = par_id
                    
                    # --- VERIFICAÇÃO DE PODA ---
                    # Antes de prosseguir, verifica se esse passo "matou" outro par
                    if not self.check_isolation(par_id):
                        # Se não isolou ninguém, continua a recursão (Deep Search)
                        if self.solve(par_index, (nl, nc)):
                            return True
                    
                    # --- BACKTRACKING ---
                    # Se a recursão falhou ou houve isolamento, desfaz a alteração (limpa a célula)
                    self.game.grid[nl][nc] = 0

        return False

# --- Configuração de Execução ---
if __name__ == "__main__":
    # Exemplo de Puzzle 6x6
    print("\n=== Puzzle NumberLink ===")
    pares = {
        1: [(0, 0), (4, 0)],
        2: [(0, 4), (4, 4)],
        3: [(2, 1), (2, 3)]
    }

    # Inicializa Jogo e Fila de Prioridade
    game = NumberLink(6, 6, pares)
    pq = PriorityQueue()
    
    # Preenche a fila baseada na distância dos pares
    for par_id in game.pares.keys():
        p1 = game.pares[par_id][0]
        p2 = game.pares[par_id][1]
        pq.enqueue(Node(p1, p2, par_id))

    # Extrai ordem de resolução
    pq_pares = []
    while True:
        node = pq.dequeue()
        if node is None: break
        pq_pares.append(node.id)

    # Inicia o Autômato
    automato = Automato(game, pq_pares)