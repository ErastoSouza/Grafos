import heapq
import random

def dijkstra(grafo, inicio):

  # Inicializa o dicionário de custos com infinito para todos os vértices, exceto o vértice inicial, que tem custo 0.
  custos = {v: float('inf') for v in grafo}
  custos[inicio] = 0

  # Inicializa a fila de prioridade com o vértice inicial.
  fila_prioridade = [(0, inicio)]

  # Enquanto a fila de prioridade não estiver vazia, repita os seguintes passos:
  while fila_prioridade:
    # Remove o vértice com o menor custo da fila de prioridade.
    custo_atual, vertice_atual = heapq.heappop(fila_prioridade)

    # Se o custo atual for maior do que o custo conhecido para o vértice atual, ignore-o.
    if custo_atual > custos[vertice_atual]:
      continue

    # Para cada vizinho do vértice atual, calcule o custo do caminho do vértice inicial para o vizinho.
    for vizinho, peso in grafo[vertice_atual][1]: 
      custo_novo = custo_atual + peso

      # Se o custo do caminho do vértice inicial para o vizinho for menor do que o custo conhecido, atualize o custo conhecido e adicione o vizinho à fila de prioridade.
      if custo_novo < custos[vizinho]:
        custos[vizinho] = custo_novo
        heapq.heappush(fila_prioridade, (custo_novo, vizinho))

  # Retorna o dicionário de custos.
  return custos

def criarPostos(postos, grafo):
  
  while len(postos) < 3:
    x = random.randint(1, len(grafo))
    postos.add(x)

def criarLagos(lagos, qlagos, postos, grafo):

  while len(lagos) != qlagos:
      x = random.randint(1, len(grafo))
      if x in postos:
        continue
      else:
        lagos.add(x)
      
def criarFogo(fogo,lagos, postos, grafo):
  while fogo == -1:
      x = random.randint(1, len(grafo))
      if x in lagos or x in postos:
        continue
      else:
        return x
      
class equipe:
  def __init__(self, posicao, capacidade, caminho):
    self.posicao
    self.capacidade
    self.caminho = []
  
  def andar():
    dijkstra()


# Cria um grafo ponderado.
grafo = {
  'A': ((4, False, False, True, 0), [('B', 5), ('C', 2)]),
  'B': ((4, False, False, True, 0), [('A', 5), ('D', 1), ('E', 3)]),
  'C': ((4, False, False, True, 0), [('A', 2), ('D', 4), ('E', 1)]),
  'D': ((4, False, False, True, 0), [('B', 1), ('C', 4)]),
  'E': ((3, False, False, False, 0), [('B', 3), ('C', 1)])
}
qlagos = 1
fogo  = -1
lagos = set()
postos = set()

criarPostos(postos, grafo)

criarLagos(lagos, qlagos, postos, grafo)

fogo = criarFogo(fogo, lagos, postos, grafo)

print(postos)

print (lagos)

print(fogo)
custos = dijkstra(grafo, 'A')

# Imprime os custos.
print(custos)