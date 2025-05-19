import random

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