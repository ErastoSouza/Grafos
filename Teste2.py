import heapq
import random
from collections import deque

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
 while len(postos) < 3:
  x = random.randint(0, len(grafo)-1)
  postos.add(x)
  grafo[chr(65+x)][0][1] = True

def criarLagos(lagos, qlagos, postos, grafo):
 while len(lagos) != qlagos:
   x = random.randint(0, len(grafo)-1)
   if x in postos:
    continue
   else:
    lagos.add(x)
    grafo[chr(65+x)][0][2] = True

def criarFogo(lagos, postos, grafo):
 while True:
   x = random.randint(0, len(grafo)-1)
   if x in lagos or x in postos:
    continue
   else:
    grafo[chr(65+x)][0][3] = 1
    break

class equipe:
 def __init__(self, posicao, capacidade):
  self.posicao = posicao
  self.capacidade = capacidade
  self.caminho = None
  self.capacidade_atual = capacidade

 def __repr__(self):
  return f"Equipe(posicao='{self.posicao}', capacidade_atual={self.capacidade_atual}/{self.capacidade})"

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

  else:
   print("Não encontrou uma estação de reabastecimento acessível. Aguardando.")

 def apagar(self, grafo):
  print(f"--- Equipe em {self.posicao}: Apagar Fogo ---")

  fogo_atual = grafo[self.posicao][0][0]

  print(f"Tentando apagar {fogo_atual} de fogo com {self.capacidade_atual} de água.")

  if fogo_atual > self.capacidade_atual:
   grafo[self.posicao][0][0] -= self.capacidade_atual
   print(f"Água insuficiente. Fogo reduzido para {grafo[self.posicao][0][0]}.")
   self.capacidade_atual = 0
   print("Água acabou.")

  else:
   self.capacidade_atual -= fogo_atual
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
 for i in grafo:
   if grafo[i][0][3] == 1:
    for j in grafo[i][1]:
      vizinho = j[0]
      x = random.randint(0,1)
      if x:
       if not grafo[vizinho][0][1] and not grafo[vizinho][0][2] and grafo[vizinho][0][3] == 0:
        grafo[vizinho][0][3] = 1
        print("Novo grafo pegando fogo")

def ta_pegando_fogo(grafo):
 for i in grafo:
  if grafo[i][0][3] == 1:
    return 1
 return 0

# Cria um grafo ponderado. {Nome do vertice : ((valor dentro do vertice, posto, lago, estado do fogo(0 = se nao pegou fogo, 1 se esta pegando fogo, -1 se já pegou fogo, 2 se queimou)))


grafo = {
 'A': [[4, False, False, 0], [('B', 5), ('C', 2), ('F', 3), ('I', 5)]],
 'B': [[4, False, False, 0], [('A', 5), ('D', 1), ('E', 3)]],
 'C': [[4, False, False, 0], [('A', 2), ('D', 4), ('E', 1), ('G', 3)]], 
 'D': [[4, False, False, 0], [('B', 1), ('C', 4), ('H', 4)]], 
 'E': [[3, False, False, 0], [('B', 3), ('C', 1), ('F', 4), ('G', 2)]], 
 'F': [[2, False, False, 0], [('A', 3), ('E', 4)]],
 'G': [[3, False, False, 0], [('C', 3), ('E', 2), ('H', 1)]], 
 'H': [[5, False, False, 0], [('D', 4), ('G', 1), ('I', 3)]], 
 'I': [[2, False, False, 0], [('A', 5), ('H', 3)]]  
}

qlagos = 0
lagos = set()
postos = set()
capacidade = 2

criarPostos(postos, grafo)
criarLagos(lagos, qlagos, postos, grafo)
criarFogo( lagos, postos, grafo)

equipes = []
auxpostos = []
for i in postos:
 auxpostos.append(i)

for i in auxpostos:
 nome_vertice = chr(65 + i)
 nova_equipe = equipe(nome_vertice, capacidade)
 equipes.append(nova_equipe)

print(equipes)

parada = 1
turno = 0
while parada:
 turno +1
 for time in equipes:
  time.andar(grafo)
 parada = ta_pegando_fogo(grafo)

 propagacao(grafo)


print(grafo)