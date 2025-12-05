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
    

# Puzzle 6x6 complexo
print("\n\nPuzzle 6x6")
pares3 = {
    1: [(0, 1), (5, 1)],
    2: [(1, 0), (1, 5)],
    3: [(2, 2), (4, 4)],
    4: [(0, 4), (3, 0)],
}
puzzle3 = NumberLink(6, 6, pares3)
puzzle3.display()
