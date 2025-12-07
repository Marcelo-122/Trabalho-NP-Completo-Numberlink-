class NumberLink:
    def __init__(self, ql, qc, pares:dict):
        """
        Inicializa o jogo NumberLink
        
        Args:
            ql: qtd_linhas,
            qc: qtd_colunas,
            pares: dicionário {id: [(x1, y1), (x2, y2)]}
                   onde cada id representa um par de pontos a conectar
        """
        self.qtd_linhas = ql
        self.qtd_colunas = qc
        self.grid = [[0] * qc for _ in range(ql)]
        self.pares = pares        
        # Coloca os pontos terminais no grid
        for par_id, pontos in pares.items():
            inicio, fim = pontos
            self.grid[inicio[0]][inicio[1]] = par_id
            self.grid[fim[0]][fim[1]] = par_id

    def esquerda(self, grid, ponto_inicial:tuple[int,int], par_id:int):
        """
            Realiza movimento para a esquerda:
            Args:
                grid = grid_atual,
                ponto_inicial = (linha, coluna)
                par_id = int -> pontos para conexão
            Retorno:
                novo_grid,
                pares_conexos: [par_id],
                ponto_atual: (linha, coluna)
        """

        nlinha, ncoluna = ponto_inicial[0], ponto_inicial[1]-1
        simb = str(par_id)+'⬅️'
        if(not self.is_valid_position(nlinha, ncoluna)): raise Exception("[ERRO] Movimento Inválido, ultrapassando grid")
        if(grid[nlinha][ncoluna] not in [0, simb, par_id]): raise Exception("[ERRO] Posição já preenchida")
        
        novo_grid = [linha[:] for linha in grid]
        novo_grid[nlinha][ncoluna] = simb
        
        return novo_grid, (nlinha, ncoluna)
    
    def direita(self, grid, ponto_inicial:tuple[int,int], par_id:int):
        """
            Realiza movimento para a direita:
            Args:
                grid = grid_atual,
                ponto_inicial = (linha, coluna)
                par_id = int -> pontos para conexão
            Retorno:
                novo_grid,
                pares_conexos: [par_id],
                ponto_atual: (linha, coluna)
        """
        nlinha, ncoluna = ponto_inicial[0], ponto_inicial[1]+1
        simb = str(par_id) + '➡️'
        if(not self.is_valid_position(nlinha, ncoluna)): raise Exception("[ERRO] Movimento Inválido, ultrapassando grid")
        if(grid[nlinha][ncoluna] not in [0, simb, par_id]): raise Exception("[ERRO] Posição já preenchida")
        
        novo_grid = [linha[:] for linha in grid]
        novo_grid[nlinha][ncoluna] = simb
    
        return novo_grid, (nlinha, ncoluna)

    def cima(self, grid, ponto_inicial:tuple[int,int], par_id:int):
        """
            Realiza movimento para a cima:
            Args:
                grid = grid_atual,
                ponto_inicial = (linha, coluna)
                par_id = int -> pontos para conexão
            Retorno:
                novo_grid,
                pares_conexos: [par_id],
                ponto_atual: (linha, coluna)
        """

        nlinha, ncoluna = ponto_inicial[0]-1, ponto_inicial[1]
        simb = str(par_id)+'⬆️'
        if(not self.is_valid_position(nlinha, ncoluna)): raise Exception("[ERRO] Movimento Inválido, ultrapassando grid")
        if(grid[nlinha][ncoluna] not in [0,simb, par_id]): raise Exception("[ERRO] Posição já preenchida")
        
        novo_grid = [linha[:] for linha in grid]
        novo_grid[nlinha][ncoluna] = simb
        
        return novo_grid, (nlinha, ncoluna)
    
    def baixo(self, grid, ponto_inicial:tuple[int,int], par_id:int):
        """
            Realiza movimento para a baixo:
            Args:
                grid = grid_atual,
                ponto_inicial = (linha, coluna)
                par_id = int -> pontos para conexão
            Retorno:
                novo_grid,
                pares_conexos: [par_id],
                ponto_atual: (linha, coluna)
        """
        nlinha, ncoluna = ponto_inicial[0]+1, ponto_inicial[1]
        simb = str(par_id)+'⬇️'
        if(not self.is_valid_position(nlinha, ncoluna)): raise Exception("[ERRO] Movimento Inválido, ultrapassando grid")
        if(grid[nlinha][ncoluna] not in [0, simb, par_id]): raise Exception("[ERRO] Posição já preenchida")
        
        novo_grid = [linha[:] for linha in grid]
        novo_grid[nlinha][ncoluna] = simb
        
        return novo_grid, (nlinha, ncoluna)
 
    def display(self, grid):
        """Exibe o grid de forma visual"""
        print("=" * (self.qtd_linhas * 4 + 1))
        
        for i in range(self.qtd_linhas):
            linha = "|"
            for j in range(self.qtd_colunas):
                valor = grid[i][j]
                if valor == 0:
                    linha += " . "
                else:
                    linha += f" {valor} "
                linha += "|"
            print(linha)
            print("-" * (self.qtd_linhas * 4 + 1))
        
        # print(f"\nDimensões: {self.qtd_linhas}x{self.qtd_colunas}")
        # print(f"Pares a conectar: {len(self.pares)}")
        # print("\nPares:")
        # for par_id, pontos in self.pares.items():
        #     print(f"  Par {par_id}: {pontos[0]} -> {pontos[1]}")
    
    def is_valid_position(self, linha, coluna):
        """Verifica se posição está dentro dos limites"""
        return (coluna >=0 and coluna < self.qtd_colunas) and (linha >= 0 and linha < self.qtd_linhas)
