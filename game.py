class NumberLink:
    """
    Classe que representa o estado do jogo (Tabuleiro/Grid).
    Gerencia as validações de movimento e informações sobre o ambiente.
    """
    def __init__(self, ql, qc, pares: dict):
        self.qtd_linhas = ql
        self.qtd_colunas = qc
        # Inicializa grid vazio com zeros
        self.grid = [[0] * qc for _ in range(ql)]
        self.pares = pares
        self.endpoints = set() 
        
        # Inicializa o tabuleiro colocando os pares (pontos iniciais e finais)
        for par_id, pontos in pares.items():
            inicio, fim = pontos
            self.grid[inicio[0]][inicio[1]] = par_id
            self.grid[fim[0]][fim[1]] = par_id
            # Armazena endpoints em um conjunto para acesso rápido O(1)
            self.endpoints.add(inicio)
            self.endpoints.add(fim)

    def is_valid_move(self, linha, coluna, par_id):
        """
        Verifica se um movimento para (linha, coluna) é permitido para o par_id.
        Retorna True se válido, False caso contrário.
        """
        # 1. Verifica se está dentro dos limites da matriz
        if not (0 <= linha < self.qtd_linhas and 0 <= coluna < self.qtd_colunas):
            return False
        
        val = self.grid[linha][coluna]
        
        # 2. Se a célula estiver vazia (0), o movimento é livre
        if val == 0:
            return True
        
        # 3. Se a célula contiver o próprio ID, verificamos se é o destino final.
        # Se for o destino, é válido (conectou). Se for um rastro já desenhado, é inválido.
        if val == par_id:
            if (linha, coluna) in self.endpoints:
                return True
            
        return False

    def count_free_neighbors(self, linha, coluna):
        """
        Função auxiliar para a heurística de poda.
        Conta quantos vizinhos acessíveis (vazios ou o próprio endpoint) 
        existem ao redor de uma coordenada específica.
        """
        livres = 0
        meu_id = self.grid[linha][coluna]
        
        for dl, dc in [(-1,0), (1,0), (0,-1), (0,1)]: # Cima, Baixo, Esq, Dir
            nl, nc = linha + dl, coluna + dc
            
            # Verifica limites
            if 0 <= nl < self.qtd_linhas and 0 <= nc < self.qtd_colunas:
                val = self.grid[nl][nc]
                # Conta se for vazio ou se for o ponto de conexão do par
                if val == 0:
                    livres += 1
                elif val == meu_id and (nl, nc) in self.endpoints:
                    livres += 1
        return livres

    def display(self):
        """Exibe o estado atual do grid no terminal de forma formatada."""
        print("=" * (self.qtd_colunas * 3 + 1))
        for i in range(self.qtd_linhas):
            linha_str = "|"
            for j in range(self.qtd_colunas):
                val = self.grid[i][j]
                if val == 0: linha_str += " . "
                else: linha_str += f" {val} "
            print(linha_str + "|")
        print("=" * (self.qtd_colunas * 3 + 1))