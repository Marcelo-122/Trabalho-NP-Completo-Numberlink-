class NumberLink:
    def __init__(self, ql, qc, pares: dict):
        self.qtd_linhas = ql
        self.qtd_colunas = qc
        self.grid = [[0] * qc for _ in range(ql)]
        self.pares = pares
        self.endpoints = set() 
        
        # Mapeia endpoints para verificação rápida
        for par_id, pontos in pares.items():
            inicio, fim = pontos
            self.grid[inicio[0]][inicio[1]] = par_id
            self.grid[fim[0]][fim[1]] = par_id
            self.endpoints.add(inicio)
            self.endpoints.add(fim)

    def is_valid_move(self, linha, coluna, par_id):
        # 1. Limites do mapa
        if not (0 <= linha < self.qtd_linhas and 0 <= coluna < self.qtd_colunas):
            return False
        
        val = self.grid[linha][coluna]
        
        # 2. Célula vazia é válida
        if val == 0:
            return True
        
        # 3. Se for o ID do próprio par, só é válido se for o ENDPOINT (destino)
        # Se for rastro (caminho já passado), é inválido (ciclo)
        if val == par_id:
            if (linha, coluna) in self.endpoints:
                return True
            
        return False

    def count_free_neighbors(self, linha, coluna):
        """
        Conta vizinhos livres para a heurística de isolamento.
        Retorna quantos movimentos válidos existem a partir de (linha, coluna).
        """
        livres = 0
        meu_id = self.grid[linha][coluna]
        
        for dl, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nl, nc = linha + dl, coluna + dc
            if 0 <= nl < self.qtd_linhas and 0 <= nc < self.qtd_colunas:
                val = self.grid[nl][nc]
                if val == 0:
                    livres += 1
                elif val == meu_id and (nl, nc) in self.endpoints:
                    livres += 1
        return livres

    def display(self):
        print("=" * (self.qtd_colunas * 3 + 1))
        for i in range(self.qtd_linhas):
            linha_str = "|"
            for j in range(self.qtd_colunas):
                val = self.grid[i][j]
                # Formatação visual simples
                if val == 0: linha_str += " . "
                else: linha_str += f" {val} "
            print(linha_str + "|")
        print("=" * (self.qtd_colunas * 3 + 1))