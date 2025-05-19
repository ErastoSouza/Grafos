import heapq

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

def reconstruir_caminho(pais, destino):
    caminho = [destino]
    atual = destino
    while atual != pais[atual]:
        atual = pais[atual]
        caminho.append(atual)
    return caminho[::-1]