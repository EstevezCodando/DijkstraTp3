# 📌 Algoritmo de Dijkstra Aplicado à Logística de Entregas

## 📖 Introdução

A logística de entregas exige planejamento eficiente para minimizar custos e tempo de transporte. O **Algoritmo de Dijkstra** é amplamente utilizado para calcular **rotas mais curtas** em redes de transporte, sendo ideal para encontrar **o menor caminho entre um centro de distribuição e diferentes bairros**.

Neste documento, detalhamos a implementação desse algoritmo para um sistema de logística, modelando a cidade como um **grafo**, onde:
- **Os vértices representam bairros**.
- **As arestas representam ruas**, com pesos indicando a **distância** entre os pontos.

---

## 📚 Fundamentação Teórica

O **Algoritmo de Dijkstra** é um **algoritmo de caminho mínimo** em grafos ponderados, que encontra a menor distância de um vértice de origem para todos os outros vértices.

### 🔹 **Funcionamento**
1. Define-se a **origem** com distância `0` e todos os outros vértices com **distância infinita**.
2. Utiliza-se uma **fila de prioridade** para processar o vértice com a **menor distância conhecida**.
3. Para cada vizinho do vértice processado, verifica-se se a **nova distância** é menor que a anterior e, caso positivo, atualiza-se a distância.
4. O processo continua até que todos os vértices tenham sido processados.

### 🔹 **Complexidade do Algoritmo**
A implementação utilizando **heap de prioridade** (`heapq`) possui complexidade **O((V + E) log V)**, onde:
- `V` é o número de vértices (bairros),
- `E` é o número de arestas (ruas).

---

## 🛠 Modelagem do Problema

O sistema é estruturado como um **grafo não-direcionado**, onde cada **bairro** é um vértice e cada **rua** uma aresta com peso representando a **distância**.

A implementação do grafo utiliza um **dicionário de adjacências**, onde cada **chave** é um bairro e os **valores** são listas de tuplas `(vizinho, distância)`.

Exemplo:
```python
grafo = {
    "Centro": [("Bairro A", 4), ("Bairro B", 2)],
    "Bairro A": [("Centro", 4), ("Bairro B", 5), ("Bairro C", 10)],
    "Bairro B": [("Centro", 2), ("Bairro A", 5), ("Bairro C", 3), ("Bairro D", 7)],
    "Bairro C": [("Bairro A", 10), ("Bairro B", 3), ("Bairro D", 8)],
    "Bairro D": [("Bairro B", 7), ("Bairro C", 8)]
}
```

---

## 🚀 Implementação

A implementação é dividida em três partes principais:

### 🔹 **1. Representação do Grafo**
O grafo é representado por uma **classe `Grafo`**, que permite adicionar **bairros e ruas** com suas respectivas distâncias.

```python
class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_aresta(self, origem: str, destino: str, distancia: float):
        """ Adiciona uma aresta bidirecional entre bairros. """
        if origem not in self.vertices:
            self.vertices[origem] = []
        if destino not in self.vertices:
            self.vertices[destino] = []
        self.vertices[origem].append((destino, distancia))
        self.vertices[destino].append((origem, distancia))  
```

### 🔹 **2. Implementação do Algoritmo de Dijkstra**
A função `dijkstra()` encontra a menor distância entre um bairro inicial e os demais.

```python
import heapq

def dijkstra(self, origem: str):
    """ Aplica Dijkstra para encontrar o menor caminho do centro de distribuição. """
    distancias = {bairro: float('inf') for bairro in self.vertices}
    distancias[origem] = 0
    caminho_anterior = {bairro: None for bairro in self.vertices}
    fila_prioridade = [(0, origem)]

    while fila_prioridade:
        distancia_atual, bairro_atual = heapq.heappop(fila_prioridade)

        for vizinho, peso in self.vertices[bairro_atual]:
            distancia_nova = distancia_atual + peso
            if distancia_nova < distancias[vizinho]:
                distancias[vizinho] = distancia_nova
                caminho_anterior[vizinho] = bairro_atual
                heapq.heappush(fila_prioridade, (distancia_nova, vizinho))

    return distancias, caminho_anterior
```

### 🔹 **3. Reconstrução do Caminho**
A função `menor_caminho()` permite reconstruir o trajeto percorrido.

```python
def menor_caminho(self, origem: str, destino: str):
    """ Retorna o menor caminho e a distância entre origem e destino. """
    distancias, caminho_anterior = self.dijkstra(origem)
    caminho = []
    bairro_atual = destino

    while bairro_atual:
        caminho.insert(0, bairro_atual)
        bairro_atual = caminho_anterior[bairro_atual]

    return caminho, distancias[destino]
```

---

## 📊 **Testes e Resultados**
Abaixo está um exemplo de teste do algoritmo:

```python
if __name__ == "__main__":
    grafo = Grafo()

    # Adicionando bairros e ruas (distâncias em km)
    grafo.adicionar_aresta("Centro", "Bairro A", 4)
    grafo.adicionar_aresta("Centro", "Bairro B", 2)
    grafo.adicionar_aresta("Bairro A", "Bairro B", 5)
    grafo.adicionar_aresta("Bairro A", "Bairro C", 10)
    grafo.adicionar_aresta("Bairro B", "Bairro C", 3)
    grafo.adicionar_aresta("Bairro C", "Bairro D", 8)
    grafo.adicionar_aresta("Bairro B", "Bairro D", 7)

    origem = "Centro"
    destino = "Bairro D"
    
    distancias, _ = grafo.dijkstra(origem)
    caminho, distancia_total = grafo.menor_caminho(origem, destino)

    print(f"\n📍 **Menores distâncias do {origem} até cada bairro:**")
    for bairro, distancia in distancias.items():
        print(f"➡️ {bairro}: {distancia} km")

    print(f"\n🛣 **Menor caminho de {origem} até {destino}:** {caminho}")
    print(f"📏 **Distância total:** {distancia_total} km")
```

---

## 🔎 **Conclusão**
A implementação do **Algoritmo de Dijkstra** permitiu determinar **o menor caminho entre um centro de distribuição e bairros**, fornecendo um sistema eficiente para logística de entregas.
