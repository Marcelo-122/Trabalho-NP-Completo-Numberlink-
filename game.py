from collections import deque

class NumberLink:
    """
    Representa o tabuleiro do jogo e contém as validações de estado.
    """
    def __init__(self, ql, qc, pares: dict):
        self.qtd_linhas = ql
        self.qtd_colunas = qc
        self.grid = [[0] * qc for _ in range(ql)]
        self.pares = pares
        self.endpoints = set() 
        
        # Inicializa o grid com os pontos fixos (Início e Fim)
        for par_id, pontos in pares.items():
            inicio, fim = pontos
            self.grid[inicio[0]][inicio[1]] = par_id
            self.grid[fim[0]][fim[1]] = par_id
            self.endpoints.add(inicio)
            self.endpoints.add(fim)

    def is_valid_move(self, linha, coluna):
        """Verifica se a coordenada está dentro dos limites do tabuleiro."""
        return 0 <= linha < self.qtd_linhas and 0 <= coluna < self.qtd_colunas

    def check_connectivity(self, current_par_id):
        """
        Validação Global (BFS - Busca em Largura).
        Verifica se ainda existe um caminho possível para todos os pares não resolvidos.
        Retorna False se algum par ficou isolado (impossível de conectar).
        """
        for pid, (start, end) in self.pares.items():
            if pid == current_par_id: continue 
            
            # Inicia BFS a partir do ponto inicial do par
            fila = deque([start])
            visitados = {start}
            encontrou = False
            
            while fila:
                r, c = fila.popleft()
                
                if (r, c) == end:
                    encontrou = True
                    break
                
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    
                    if self.is_valid_move(nr, nc):
                        if (nr, nc) not in visitados:
                            val = self.grid[nr][nc]
                            # Pode transitar se for vazio (0), o próprio par, ou o destino
                            if val == 0 or val == pid:
                                visitados.add((nr, nc))
                                fila.append((nr, nc))
            
            if not encontrou:
                return False # Detectou isolamento
        
        return True

    def display(self):
        """Exibe o grid formatado no terminal."""
        print("=" * (self.qtd_colunas * 3 + 1))
        for i in range(self.qtd_linhas):
            linha_str = "|"
            for j in range(self.qtd_colunas):
                val = self.grid[i][j]
                linha_str += " . " if val == 0 else f" {val} "
            print(linha_str + "|")
        print("=" * (self.qtd_colunas * 3 + 1))