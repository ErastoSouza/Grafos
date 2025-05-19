from dijkstra import dijkstra, reconstruir_caminho

class equipe:
    def __init__(self, posicao, capacidade):
        self.posicao = posicao
        self.capacidade = capacidade
        self.caminho = None
        self.capacidade_atual = capacidade
        self.agua_usada = 0

    def __repr__(self):
        return f"Equipe(posicao='{self.posicao}', capacidade_atual={self.capacidade_atual}/{self.capacidade}, água={self.agua_usada})"

    def andar(self, grafo):
        print(f"\n--- Equipe em {self.posicao} ---")

        if self.capacidade_atual == 0:
            print("Sem água, procurando reabastecer.")
            self.reabastecer(grafo)
            return

        if grafo[self.posicao][0][3] == 1 and self.capacidade_atual > 0:
            print("No local do fogo e com água.")
            self.apagar(grafo)
            return

        print("Procurando o fogo mais próximo.")
        custo, pais = dijkstra(grafo, self.posicao)
        custo_minimo_fogo = float("inf")
        destino_fogo = None

        for vertice in grafo:
            if grafo[vertice][0][3] == 1 and custo[vertice] != float('inf'):
                if custo[vertice] < custo_minimo_fogo:
                    custo_minimo_fogo = custo[vertice]
                    destino_fogo = vertice

        if destino_fogo is not None:
            print(f"Fogo detectado em {destino_fogo}. Indo para lá.")
            self.caminho = reconstruir_caminho(pais, destino_fogo)

            if len(self.caminho) > 1:
                proximo_vertice = self.caminho[1]
                print(f"Movendo de {self.posicao} para {proximo_vertice}.")
                self.posicao = proximo_vertice
            else:
                print(f"Já no destino do fogo {destino_fogo}. Verificando...")
                if grafo[self.posicao][0][3] == 1 and self.capacidade_atual > 0:
                    self.apagar(grafo)

        else:
            print("Sem fogos ativos conhecidos e com água. Aguardando.")

    def reabastecer(self, grafo):
        print(f"--- Equipe em {self.posicao}: Reabastecer ---")
        custo, pais = dijkstra(grafo, self.posicao)
        min_custo = float("inf")
        destino_reabastecer = None

        for vertice in grafo:
            if (grafo[vertice][0][1] is True or grafo[vertice][0][2] is True) and custo[vertice] != float('inf'):
                if custo[vertice] < min_custo:
                    min_custo = custo[vertice]
                    destino_reabastecer = vertice

        if destino_reabastecer is not None:
            print(f"Estação de reabastecimento detectada em {destino_reabastecer}. Indo para lá.")
            self.caminho = reconstruir_caminho(pais, destino_reabastecer)

            if len(self.caminho) > 1:
                proximo_vertice = self.caminho[1]
                print(f"Movendo de {self.posicao} para {proximo_vertice} para reabastecer.")
                self.posicao = proximo_vertice
            else:
                print(f"Chegou na estação de reabastecimento {destino_reabastecer}. Reabastecendo!")
                self.capacidade_atual = self.capacidade
                print(f"Reabastecido. Capacidade atual: {self.capacidade_atual}/{self.capacidade}.")

    def apagar(self, grafo):
        print(f"--- Equipe em {self.posicao}: Apagar Fogo ---")

        fogo_atual = grafo[self.posicao][0][0]

        print(f"Tentando apagar {fogo_atual} de fogo com {self.capacidade_atual} de água.")

        if fogo_atual > self.capacidade_atual:
            grafo[self.posicao][0][0] -= self.capacidade_atual
            self.agua_usada += self.capacidade_atual
            print(f"Água insuficiente. Fogo reduzido para {grafo[self.posicao][0][0]}.")
            self.capacidade_atual = 0
            print("Água acabou.")

        else:
            self.capacidade_atual -= fogo_atual
            self.agua_usada += fogo_atual
            grafo[self.posicao][0][0] = 0
            grafo[self.posicao][0][3] = -1
            print(f"Fogo em {self.posicao} apagado!")
            print(f"Restam {self.capacidade_atual} de água.")