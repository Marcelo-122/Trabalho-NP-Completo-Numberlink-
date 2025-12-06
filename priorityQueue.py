class Node:
    def __init__(self, p1:tuple[int,int],p2:tuple[int,int], id):
        self.id = id
        self.ponto_inicial = p1
        self.ponto_final = p2
        self.dist = self.distancia_manhattan(p1,p2)
    
    def distancia_manhattan(self, p1:tuple[int,int],p2:tuple[int,int]):
        """
        Calcula distância de Manhattan entre dois pontos
        |x1 - x2| + |y1 - y2|
        """
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def __lt__(self,other):
        return self.dist < other.dist

class PriorityQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item:Node):
        self.items.append(item)
        self.items.sort()
    
    def dequeue(self)->Node:
        if(len(self.items) == 0):
            return None
        return self.items.pop(0)
