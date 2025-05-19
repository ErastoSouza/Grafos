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