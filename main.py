import json
from preparacao import criarPostos, criarLagos, criarFogo
from equipe import equipe
from fogo import propagacao, ta_pegando_fogo
from relatorio import relatorio

def main():
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

if __name__ == "__main__":
    main()