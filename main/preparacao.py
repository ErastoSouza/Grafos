import random

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