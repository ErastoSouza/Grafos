import heapq
import random
import json

def dijkstra(grafo, inicio):
    custos = {v: float('inf') for v in grafo}
    custos[inicio] = 0

    pais = {v: "none" for v in grafo}
    pais[inicio] = inicio

    fila_prioridade = [(0, inicio)]

    while fila_prioridade:
        custo_atual, vertice_atual = heapq.heappop(fila_prioridade)

        if custo_atual > custos[vertice_atual]:
            continue

        for vizinho, peso in grafo[vertice_atual][1]:
            custo_novo = custo_atual + peso

            if custo_novo < custos[vizinho]:
                custos[vizinho] = custo_novo
                pais[vizinho] = vertice_atual
                heapq.heappush(fila_prioridade, (custo_novo, vizinho))

    return custos, pais

def criarPostos(postos, grafo):
    lista_vertices = list(grafo.keys())
    while len(postos) < 3:
        vertice = random.choice(lista_vertices)
        if vertice not in postos:
            postos.add(vertice)
            grafo[vertice][0][1] = True

def criarLagos(lagos, qlagos, postos, grafo):
    lista_vertices = list(grafo.keys())
    while len(lagos) < qlagos:
        vertice = random.choice(lista_vertices)
        if vertice not in postos and vertice not in lagos:
            lagos.add(vertice)
            grafo[vertice][0][2] = True

def criarFogo(lagos, postos, grafo):
    lista_vertices = list(grafo.keys())
    while True:
        vertice = random.choice(lista_vertices)
        if vertice not in lagos and vertice not in postos:
            grafo[vertice][0][3] = 1
            break

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

def reconstruir_caminho(pais, destino):
    caminho = [destino]
    atual = destino
    while atual != pais[atual]:
        atual = pais[atual]
        caminho.append(atual)

    return caminho[::-1]

def propagacao(grafo):
    for vertice in grafo:
        if grafo[vertice][0][3] == 1:
            for vizinho, peso in grafo[vertice][1]:
                x = random.randint(0, 1)
                if x:
                    if not grafo[vizinho][0][1] and not grafo[vizinho][0][2] and grafo[vizinho][0][3] == 0:
                        grafo[vizinho][0][3] = 1
                        print(f"\nVertice {vizinho} pegando fogo🔥")

def ta_pegando_fogo(grafo):
    for vertice in grafo:
        if grafo[vertice][0][3] == 1:
            return True
    return False

def relatorio(grafo, equipes, turno):
    queimados = 0
    agua_usada = 0
    print("\n============================================================================")
    print("            Resumo de como ficou a situação final do grafo")
    print("============================================================================")
    print()
    for vertice in grafo:
        print(f"Vertice {vertice} ", end="")
        if grafo[vertice][0][1]:
            print("é um posto então tá de boa🧑‍🚒")
        elif grafo[vertice][0][2]:
            print("é um lago então tá de boa🦆")
        elif grafo[vertice][0][3] == 0:
            print("nem sequer pegou fogo, parabéns pessoal🎉")
        elif grafo[vertice][0][3] == -1:
            print(f"pegou fogo durante {grafo[vertice][0][4]} turnos, porém foi apagado a tempo😥")
        elif grafo[vertice][0][3] == 2:
            print(f"pegou fogo durante {grafo[vertice][0][4]} turnos, e queimou completamente😿")
            queimados += 1
    total_vertices = len(grafo)
    for equipe in equipes:
        agua_usada += equipe.agua_usada
    print(f"\nDos {total_vertices} vértices, foram salvos {total_vertices - queimados} e queimados {queimados}.")
    print(f"Foram usados {agua_usada} litros de água em {turno} turnos.\n")
    print("============================================================================")

# Leitura do arquivo JSON
arquivo_json = input("Digite o nome do arquivo JSON com o grafo (ex: grafo.json): ")

with open(arquivo_json, 'r') as f:
    dados = json.load(f)

# Construção do grafo
grafo = {}
for vertice in dados["grafo"]:
    nome = vertice["nome"]
    combustivel = vertice["combustivel"]
    arestas = [(a["destino"], a["peso"]) for a in vertice["arestas"]]
    grafo[nome] = [[combustivel, False, False, 0, 0], arestas]

# Configurações adicionais
capacidade = int(input("\nCapacidade de água dos caminhões: "))
qlagos = int(input("Quantidade de lagos: "))

postos = set()
lagos = set()

criarPostos(postos, grafo)
criarLagos(lagos, qlagos, postos, grafo)
criarFogo(lagos, postos, grafo)

equipes = []
for posto in postos:
    nova_equipe = equipe(posto, capacidade)
    equipes.append(nova_equipe)

print("\nEquipes inicializadas:")
print(equipes)

# Simulação
parada = True
turno = 0
while parada:
    turno += 1
    print("\n========================================")
    print(f"               Turno: {turno}")
    print("========================================")
    
    for time in equipes:
        time.andar(grafo)
        parada = ta_pegando_fogo(grafo)
        if not parada:
            print("Acabou o fogo no grafo")
            break
    
    for vertice in grafo:
        if grafo[vertice][0][3] == 1 and grafo[vertice][0][0] > 0:
            grafo[vertice][0][0] -= 1
            grafo[vertice][0][4] += 1
            if grafo[vertice][0][4] == 3 and grafo[vertice][0][3] != -1:
                grafo[vertice][0][3] = 2
                print(f"\nO vértice {vertice} parou de pegar fogo pois não foi atendido a tempo🤦‍♂️")
            elif grafo[vertice][0][0] == 0:
                grafo[vertice][0][3] = -1
                print(f"\nO vértice {vertice} parou de pegar fogo pois foi resfriado😎")
    
    print("\nStatus das equipes:")
    print(equipes)
    
    propagacao(grafo)

relatorio(grafo, equipes, turno)