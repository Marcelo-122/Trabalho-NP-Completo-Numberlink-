from game import NumberLink
from priorityQueue import PriorityQueue,Node
import random
class Automato:
    def __init__(self, game:NumberLink, pq_pares:list[int]):
        self.game = game
        self.pq_pares = pq_pares
        self.solucao = None
        pos_inicial = self.game.pares[pq_pares[0]][0]
        self.visited = set()
        print(self.DFS([linha[:] for linha in game.grid], 0, pos_inicial))

    def hash_grid(self, grid):
        return tuple(tuple(row) for row in grid)

    def DFS(self, grid, par_index, pos_atual):
        state = (self.hash_grid(grid), par_index)
        if state in self.visited: return False
        self.visited.add(state)

        par_id = self.pq_pares[par_index]
        destino = self.game.pares[par_id][1]

        # chegou no destino → próximo par
        if pos_atual == destino:
            if par_index == len(self.pq_pares)-1:
                self.solucao = grid
                return True
            self.visited = set()
            next_start = self.game.pares[self.pq_pares[par_index+1]][0]
            return self.DFS([linha[:] for linha in grid], par_index + 1, next_start)

        actions = [self.game.esquerda, self.game.direita, self.game.cima, self.game.baixo]
        
        for action in actions:
            try:
                new_grid, cur_pos = action([linha[:] for linha in grid], pos_atual, par_id)
                if(Node.distancia_manhattan(pos_atual, destino) < Node.distancia_manhattan(cur_pos, destino)): continue
            except:
                continue
            
            if self.DFS(new_grid, par_index, cur_pos):
                return True
        return False
              

# Puzzle 6x6 complexo
print("\n\nPuzzle 6x6")
pares3 = {
    1: [(0, 0), (4, 0)],
    2: [(0, 4), (4, 4)],
    3: [(2, 1), (2, 3)]
}
pq = PriorityQueue()
game = NumberLink(7, 7, pares3)
for par_id in game.pares.keys():
    p1 = game.pares[par_id][0]
    p2 = game.pares[par_id][1]
    pq.enqueue(Node(p1,p2,par_id))
pq_pares = [pq.dequeue().id for _ in range(len(pq.items))]


automato = Automato(game,pq_pares)
if(automato.solucao != None):
    automato.game.display(automato.solucao)