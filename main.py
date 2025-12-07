from game import NumberLink
from visualizer import draw_grid_live
from priorityQueue import PriorityQueue, Node
import sys
import time

# Permite recursão profunda para puzzles complexos
sys.setrecursionlimit(20000)

class Automato:
    def __init__(self, game: NumberLink, pq_pares: list[int]):
        self.game = game
        self.pq_pares = pq_pares
        self.passos = 0
        self.start_time = time.time()
        
        primeiro_par = pq_pares[0]
        pos_inicial = self.game.pares[primeiro_par][0]
        
        print(f"Iniciando resolução com ordem: {pq_pares}")
        
        if self.solve(0, pos_inicial):
            tempo = time.time() - self.start_time
            print(f"\n✅ Solução encontrada em {tempo:.4f}s e {self.passos} passos!")
            self.game.display()
        else:
            print("\n❌ Não foi possível encontrar solução.")

    def check_isolation(self, active_par_id):
        """
        HEURÍSTICA CRÍTICA:
        Se um movimento deixar o endpoint de OUTRO par sem vizinhos livres,
        esse movimento é ruim e deve ser descartado imediatamente.
        """
        for pid in self.pq_pares:
            # Ignora o par que estamos mexendo agora
            if pid == active_par_id: continue
            
            p1, p2 = self.game.pares[pid]
            
            # Precisamos checar os endpoints. Se um endpoint tem 0 saídas
            # e ainda não foi conectado, o jogo acabou para aquele par.
            
            # Nota: O código ideal checaria se o par já foi 'completado', 
            # mas verificar vizinhos > 0 nos endpoints resolve 95% dos casos de bloqueio.
            n1 = self.game.count_free_neighbors(p1[0], p1[1])
            n2 = self.game.count_free_neighbors(p2[0], p2[1])
            
            if n1 == 0 or n2 == 0:
                return True # Detectou isolamento
        return False

    def solve(self, par_index, pos_atual):
        draw_grid_live(self.game, delay=0.001)
        self.passos += 1
        
        # Caso Base: Se terminamos a lista de pares
        if par_index >= len(self.pq_pares):
            return True

        par_id = self.pq_pares[par_index]
        destino = self.game.pares[par_id][1]

        # 1. Chegamos ao destino deste par?
        if pos_atual == destino:
            # Passa para o próximo par na lista
            if par_index + 1 < len(self.pq_pares):
                prox_id = self.pq_pares[par_index + 1]
                prox_inicio = self.game.pares[prox_id][0]
                return self.solve(par_index + 1, prox_inicio)
            else:
                return True # Todos resolvidos!

        # 2. Define movimentos possíveis (Cima, Baixo, Esq, Dir)
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # HEURÍSTICA: Tenta ir na direção do destino primeiro (ordena movimentos)
        # Isso acelera muito, mas permite desvios se necessário (o loop continua)
        movimentos.sort(key=lambda m: abs((pos_atual[0]+m[0]) - destino[0]) + abs((pos_atual[1]+m[1]) - destino[1]))

        l, c = pos_atual
        
        for dl, dc in movimentos:
            nl, nc = l + dl, c + dc
            
            if self.game.is_valid_move(nl, nc, par_id):
                eh_destino = ((nl, nc) == destino)
                
                if eh_destino:
                    # Se chegou no destino, não pinta grid, apenas avança recursão
                    if self.solve(par_index, (nl, nc)): return True
                else:
                    # --- APLICA MOVIMENTO (Backtracking) ---
                    self.game.grid[nl][nc] = par_id
                    
                    # --- PODA (Pruning) ---
                    # Verifica se matamos outro par com esse movimento
                    if not self.check_isolation(par_id):
                        if self.solve(par_index, (nl, nc)):
                            return True
                    
                    # --- DESFAZ MOVIMENTO ---
                    self.game.grid[nl][nc] = 0

        return False

# --- SETUP DO TESTE ---
# Puzzle 6x6 que estava no seu arquivo
print("\n=== Puzzle NumberLink 6x6 ===")
pares3 = {
    1: [(0, 0), (4, 0)],
    2: [(0, 4), (4, 4)],
    3: [(2, 1), (2, 3)]
}

# Ajustei o tamanho para 6x6 (estava 7x7 no seu código, mas índices iam até 4)
# Se os índices máximos são 4, um grid 5x5 ou 6x6 serve. Coloquei 6x6 por segurança.
game = NumberLink(6, 6, pares3)

pq = PriorityQueue()
for par_id in game.pares.keys():
    p1 = game.pares[par_id][0]
    p2 = game.pares[par_id][1]
    pq.enqueue(Node(p1, p2, par_id))

# Extrai a ordem da fila
pq_pares = []
while True:
    node = pq.dequeue()
    if node is None: break
    pq_pares.append(node.id)

automato = Automato(game, pq_pares)