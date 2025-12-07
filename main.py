class NumberLink:
    def __init__(self, n, m, pares):
        """
        Inicializa o jogo NumberLink
        
        Args:
            n: altura do grid
            m: largura do grid
            pares: dicionário {id: [(x1, y1), (x2, y2)]}
                   onde cada id representa um par de pontos a conectar
        """
        self.n = n
        self.m = m
        self.grid = [[0] * m for _ in range(n)]
        self.pares = pares
        
        # Coloca os pontos terminais no grid
        for par_id, pontos in pares.items():
            inicio, fim = pontos
            self.grid[inicio[0]][inicio[1]] = par_id
            self.grid[fim[0]][fim[1]] = par_id
    
    def display(self):
        """Exibe o grid de forma visual"""
        print("=" * (self.m * 4 + 1))
        
        for i in range(self.n):
            linha = "|"
            for j in range(self.m):
                valor = self.grid[i][j]
                if valor == 0:
                    linha += " . "
                else:
                    linha += f" {valor} "
                linha += "|"
            print(linha)
            print("-" * (self.m * 4 + 1))
        
        print(f"\nDimensões: {self.n}x{self.m}")
        print(f"Pares a conectar: {len(self.pares)}")
        print("\nPares:")
        for par_id, pontos in self.pares.items():
            print(f"  Par {par_id}: {pontos[0]} -> {pontos[1]}")
    
    def distancia_manhattan(self, p1, p2):
        """
        Calcula distância de Manhattan entre dois pontos
        |x1 - x2| + |y1 - y2|
        """
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def is_valid_position(self, x, y):
        """Verifica se posição está dentro dos limites"""
        return 0 <= x < self.n and 0 <= y < self.m

# Puzzle 7x7 complexo
print("\n\nPuzzle 7x7")
pares3 = {
    1: [(2, 4), (5, 2)],
    2: [(1, 4), (6, 0)],
    3: [(1, 1), (2, 3)],
    4: [(0, 3), (6, 4)],
    5: [(1, 5), (3, 3)],
}
puzzle3 = NumberLink(7, 7, pares3)
puzzle3.display()

print(puzzle3.distancia_manhattan((0, 1), (5, 1)))
