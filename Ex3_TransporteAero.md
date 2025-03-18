# ✈️ **Rede de Transportes Aéreos - Algoritmo de Dijkstra**

## 📖 **Introdução**

A eficiência no planejamento de rotas aéreas é essencial para reduzir **custos operacionais**, **tempo de viagem** e **impacto ambiental**. Empresas aéreas utilizam algoritmos de otimização para determinar **o menor trajeto entre dois aeroportos**. 

Este estudo propõe a utilização do **Algoritmo de Dijkstra** para encontrar **o menor caminho em uma rede de transportes aéreos**, onde:
- **Os vértices representam aeroportos**.
- **As arestas representam rotas diretas** entre aeroportos.
- **Os pesos indicam a distância** entre os aeroportos (em quilômetros).

---

## 📚 **Fundamentação Teórica**

O **Algoritmo de Dijkstra** é um **algoritmo de menor caminho** para grafos ponderados. Ele encontra o caminho **ótimo** do **aeroporto de origem** para os demais.

### 🔹 **Funcionamento do Algoritmo**
1. Define-se a **origem** com **distância 0** e os demais aeroportos com **distância infinita**.
2. Utiliza-se uma **fila de prioridade** para sempre processar o **aeroporto mais próximo**.
3. Para cada **vizinho do aeroporto atual**, verifica-se se **o novo caminho é mais curto** do que o previamente armazenado. Caso seja, **atualiza-se a distância**.
4. O algoritmo continua até que **todos os aeroportos tenham sido processados**.

### 🔹 **Complexidade Computacional**
A implementação usando **fila de prioridade (`heapq`)** possui complexidade **O((V + E) log V)**, onde:
- `V` → Número de aeroportos.
- `E` → Número de conexões entre aeroportos.

---

## 🛠 **Modelagem do Problema**

A malha aérea é representada como um **grafo não-direcionado**, onde **cada aeroporto é um vértice** e **cada conexão direta é uma aresta** ponderada com **distância em quilômetros**.

A modelagem utiliza um **dicionário de adjacências**, onde cada **chave** representa um aeroporto e os **valores** são listas de aeroportos conectados e suas respectivas distâncias.

### **Exemplo de Representação**
```python
rede = {
    "GRU": [("GIG", 365), ("BSB", 873)],
    "GIG": [("GRU", 365), ("CNF", 440)],
    "BSB": [("GRU", 873), ("CNF", 624), ("SSA", 1060)],
    "CNF": [("GIG", 440), ("BSB", 624), ("SSA", 694)],
    "SSA": [("BSB", 1060), ("CNF", 694), ("REC", 675)],
    "REC": [("SSA", 675)]
}
```

---

## 🚀 **Implementação do Algoritmo**

A implementação é dividida em três partes:

### 🔹 **1. Classe `RedeAerea`**
Essa classe representa a **rede de aeroportos e distâncias diretas entre eles**.

```python
class RedeAerea:
    def __init__(self):
        self.aeroportos = {}

    def adicionar_rota(self, origem: str, destino: str, distancia: float):
        """ Adiciona uma conexão direta entre dois aeroportos. """
        if origem not in self.aeroportos:
            self.aeroportos[origem] = []
        if destino not in self.aeroportos:
            self.aeroportos[destino] = []
        self.aeroportos[origem].append((destino, distancia))
        self.aeroportos[destino].append((origem, distancia))
```

---

### 🔹 **2. Algoritmo de Dijkstra**
A função `dijkstra()` encontra **o menor caminho entre um aeroporto de origem e todos os demais**.

```python
import heapq

def dijkstra(self, origem: str):
    """ Aplica Dijkstra para encontrar a menor distância entre aeroportos. """
    distancias = {aeroporto: float('inf') for aeroporto in self.aeroportos}
    distancias[origem] = 0
    caminho_anterior = {aeroporto: None for aeroporto in self.aeroportos}
    fila_prioridade = [(0, origem)]

    while fila_prioridade:
        distancia_atual, aeroporto_atual = heapq.heappop(fila_prioridade)

        for vizinho, peso in self.aeroportos[aeroporto_atual]:
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                caminho_anterior[vizinho] = aeroporto_atual
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

    return distancias, caminho_anterior
```

---

### 🔹 **3. Reconstrução do Menor Caminho**
A função `menor_rota()` permite **reconstruir o trajeto mais curto**.

```python
def menor_rota(self, origem: str, destino: str):
    """ Retorna a menor rota e a distância total. """
    distancias, caminho_anterior = self.dijkstra(origem)
    caminho = []
    aeroporto_atual = destino

    while aeroporto_atual:
        caminho.insert(0, aeroporto_atual)
        aeroporto_atual = caminho_anterior[aeroporto_atual]

    return caminho, distancias[destino]
```

---

## 📊 **Testes e Resultados**
Abaixo está um exemplo de execução do algoritmo:

```python
if __name__ == "__main__":
    rede = RedeAerea()
    rede.adicionar_rota("GRU", "GIG", 365)
    rede.adicionar_rota("GRU", "BSB", 873)
    rede.adicionar_rota("GIG", "CNF", 440)
    rede.adicionar_rota("BSB", "CNF", 624)
    rede.adicionar_rota("BSB", "SSA", 1060)
    rede.adicionar_rota("CNF", "SSA", 694)
    rede.adicionar_rota("SSA", "REC", 675)

    origem = "GRU"
    destino = "REC"

    tempos, _ = rede.dijkstra(origem)
    caminho, distancia_total = rede.menor_rota(origem, destino)

    print(f"\n📍 **Menores distâncias a partir do aeroporto {origem}:**")
    for aeroporto, distancia in tempos.items():
        print(f"➡️ {aeroporto}: {distancia} km")

    print(f"\n✈️ **Melhor rota de {origem} até {destino}:** {caminho}")
    print(f"📏 **Distância total:** {distancia_total} km")
```

---

## 🔎 **Conclusão**
A aplicação do **Algoritmo de Dijkstra** permitiu encontrar **a menor rota entre aeroportos**, otimizando **tempo de voo e planejamento de viagens**.

