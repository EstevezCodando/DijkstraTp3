# 🚍 Roteamento de Ônibus - Algoritmo de Dijkstra

## 📖 Introdução

O planejamento de rotas eficientes para transporte público é essencial para otimizar **tempo de deslocamento, custo operacional e experiência dos passageiros**. O **Algoritmo de Dijkstra** é amplamente utilizado para encontrar **o menor caminho em grafos ponderados**, sendo ideal para determinar **a rota mais rápida entre dois bairros movimentados**.

Este estudo propõe um modelo de cidade como um **grafo**, onde:
- **Os vértices representam bairros**.
- **As arestas representam ruas**, ponderadas pelo **tempo médio de deslocamento**.

A solução computacional permite encontrar o **trajeto mais curto** e pode ser aplicada a **planejamento de linhas de ônibus**, **sistemas de GPS** e **logística urbana**.

---

## 📚 Fundamentação Teórica

O **Algoritmo de Dijkstra** é um método de **busca de menor caminho** para **grafos ponderados**, garantindo que o trajeto encontrado seja **ótimo**.

### 🔹 **Funcionamento**
1. Define-se um **bairro de origem** com **tempo de deslocamento 0** e os demais com **tempo infinito**.
2. Utiliza-se uma **fila de prioridade** para sempre processar o **bairro mais próximo**.
3. Para cada vizinho do bairro atual, verifica-se se **o tempo total até ele** é menor que o anterior e, caso positivo, **atualiza-se a informação**.
4. O algoritmo continua até que **todos os bairros tenham sido processados**.

### 🔹 **Complexidade Computacional**
- A implementação com **fila de prioridade (`heapq`)** tem complexidade **O((V + E) log V)**, onde:
  - `V` → número de bairros,
  - `E` → número de ruas.

---

## 🛠 Modelagem do Problema

A cidade é representada por um **grafo não-direcionado**, onde cada **bairro** é um vértice e cada **rua** é uma aresta com peso baseado no **tempo médio de deslocamento (minutos)**.

A estrutura de dados utilizada é um **dicionário de adjacências**, no qual cada **chave** representa um bairro e os **valores** são listas de **bairros vizinhos e tempos médios**.

Exemplo:
```python
grafo = {
    "Bairro A": [("Bairro B", 10), ("Bairro C", 15)],
    "Bairro B": [("Bairro A", 10), ("Bairro D", 12), ("Bairro C", 5)],
    "Bairro C": [("Bairro A", 15), ("Bairro B", 5), ("Bairro D", 10), ("Bairro E", 5)],
    "Bairro D": [("Bairro B", 12), ("Bairro C", 10), ("Bairro E", 10)],
    "Bairro E": [("Bairro C", 5), ("Bairro D", 10)]
}
```

---

## 🚀 Implementação

A implementação é composta por três módulos principais:

### 🔹 **1. Classe `Grafo`**
O grafo é representado pela classe `Grafo`, que permite a **criação de bairros e ruas**.

```python
class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_aresta(self, origem: str, destino: str, tempo: float):
        """ Adiciona uma aresta representando o tempo médio entre dois bairros. """
        if origem not in self.vertices:
            self.vertices[origem] = []
        if destino not in self.vertices:
            self.vertices[destino] = []
        self.vertices[origem].append((destino, tempo))
        self.vertices[destino].append((origem, tempo))
```

### 🔹 **2. Algoritmo de Dijkstra**
A função `dijkstra()` encontra o menor tempo entre um **bairro de origem** e todos os demais.

```python
import heapq

def dijkstra(self, origem: str):
    """ Calcula o menor tempo de deslocamento do bairro de origem para os demais. """
    tempos = {bairro: float('inf') for bairro in self.vertices}
    tempos[origem] = 0
    caminho_anterior = {bairro: None for bairro in self.vertices}
    fila_prioridade = [(0, origem)]

    while fila_prioridade:
        tempo_atual, bairro_atual = heapq.heappop(fila_prioridade)

        for vizinho, peso in self.vertices[bairro_atual]:
            novo_tempo = tempo_atual + peso
            if novo_tempo < tempos[vizinho]:
                tempos[vizinho] = novo_tempo
                caminho_anterior[vizinho] = bairro_atual
                heapq.heappush(fila_prioridade, (novo_tempo, vizinho))

    return tempos, caminho_anterior
```

### 🔹 **3. Reconstrução do Menor Caminho**
A função `menor_caminho()` permite **reconstruir o trajeto mais curto**.

```python
def menor_caminho(self, origem: str, destino: str):
    """ Retorna o menor trajeto e o tempo total de deslocamento. """
    tempos, caminho_anterior = self.dijkstra(origem)
    caminho = []
    bairro_atual = destino

    while bairro_atual:
        caminho.insert(0, bairro_atual)
        bairro_atual = caminho_anterior[bairro_atual]

    return caminho, tempos[destino]
```

---

## 📊 **Testes e Resultados**
Exemplo de teste do algoritmo:

```python
if __name__ == "__main__":
    grafo = Grafo()
    grafo.adicionar_aresta("Bairro A", "Bairro B", 10)
    grafo.adicionar_aresta("Bairro A", "Bairro C", 15)
    grafo.adicionar_aresta("Bairro B", "Bairro D", 12)
    grafo.adicionar_aresta("Bairro B", "Bairro C", 5)
    grafo.adicionar_aresta("Bairro C", "Bairro D", 10)
    grafo.adicionar_aresta("Bairro C", "Bairro E", 5)
    grafo.adicionar_aresta("Bairro D", "Bairro E", 10)

    origem = "Bairro A"
    destino = "Bairro E"
    
    tempos, _ = grafo.dijkstra(origem)
    caminho, tempo_total = grafo.menor_caminho(origem, destino)

    print(f"\n📍 **Menores tempos de deslocamento a partir de {origem}:**")
    for bairro, tempo in tempos.items():
        print(f"➡️ {bairro}: {tempo} minutos")

    print(f"\n🚌 **Menor trajeto de {origem} até {destino}:** {caminho}")
    print(f"⏱ **Tempo total de deslocamento:** {tempo_total} minutos")
```

---

## 🔎 **Conclusão**
A aplicação do **Algoritmo de Dijkstra** permitiu encontrar **o trajeto mais rápido entre dois bairros movimentados**, garantindo um **planejamento otimizado para transporte público**.
