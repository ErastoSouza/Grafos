# Grafos
Trabalho da cadeira de Algoritmos em grafos do curso de Matemática Computacional no período 2024.2

# 🔥 Simulador de Combate a Incêndios em Grafos

Este projeto implementa um sistema de simulação de combate a incêndios em estruturas representadas por grafos. Utilizando diferentes configurações de grafos (circular, estrela, qualquer formato), o sistema avalia a propagação do fogo e a resposta de equipes de combate com deslocamento inteligente baseado no algoritmo de Dijkstra.

## 📁 Estrutura do Projeto

- `main.py`: script principal que executa a simulação.
- `GrafoCircular.json`: grafo circular com 10 vértices conectados em forma de anel.
- `Grafo_Estrela.json`: grafo com vértices conectados a um centro (estrela).
- `Grafo_Qualquer1.json`, `Grafo_Qualquer2.json`: grafos genéricos para testes variados.
- `LICENSE`: licença de uso do projeto.

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/ErastoSouza/Grafos.git
cd Grafo
cd main
```

2. Execute o script:

```bash
python3 main.py
```

3. Ao executar, será solicitado:

- Nome do arquivo `.json` do grafo (ex: `GrafoCircular.json`)
- Capacidade de água dos caminhões
- Quantidade de lagos

A simulação então inicia por turnos automáticos.

## 🌐 Estrutura do Grafo JSON

Cada grafo é representado como uma lista de vértices:

```json
{
  "nome": "A1",
  "combustivel": 5,
  "arestas": [
    {"destino": "A2", "peso": 3},
    {"destino": "A3", "peso": 4}
  ]
}
```

- `nome`: identificador do vértice
- `combustivel`: quantidade inicial de fogo potencial
- `arestas`: conexões para outros vértices com pesos (distâncias)

## 🚒 Dinâmica da Simulação

- **Equipes** partem de postos gerados aleatoriamente
- **Lagos** são pontos de reabastecimento de água
- **Fogo** inicia aleatoriamente e se propaga para vizinhos
- Cada turno:
  - Equipes se movem com base no menor caminho (Dijkstra)
  - Combatem o fogo ou reabastecem
  - O fogo se propaga estocasticamente
  - Após 3 turnos em chamas sem combate, o vértice queima completamente

## 📈 Saída

A simulação imprime o status a cada turno e gera um relatório final como:

```
Vertice A é um posto então tá de boa🧑‍🚒
Vertice B pegou fogo durante 2 turnos, porém foi apagado a tempo😥
Vertice C pegou fogo durante 3 turnos, e queimou completamente😿

Dos 10 vértices, foram salvos 8 e queimados 2.
Foram usados 12 litros de água em 6 turnos.
```