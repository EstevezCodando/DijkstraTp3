# 🚛 **Transporte de Mercadorias - Algoritmo de Dijkstra**

## 📖 **Introdução**

A logística de transporte de mercadorias exige planejamento eficiente para minimizar **custos operacionais, tempo de deslocamento e consumo de combustível**. Para caminhoneiros e empresas de transporte, a escolha da **rota mais econômica** pode representar **redução de custos e aumento da eficiência**.

Este estudo aplica o **Algoritmo de Dijkstra** para determinar **a rota mais barata entre duas cidades**, considerando:
- **Vértices (nós)** → Cidades.
- **Arestas (ligações entre cidades)** → Rodovias.
- **Pesos das arestas** → Custo da viagem (pedágios + combustível).

---

## 📚 **Fundamentação Teórica**

O **Algoritmo de Dijkstra** é um **algoritmo clássico de menor caminho** para grafos ponderados. Ele encontra **o trajeto mais econômico** garantindo que o custo total seja **mínimo**.

### 🔹 **Funcionamento do Algoritmo**
1. Define-se a **cidade de origem** com **custo 0**, e todas as demais com **custo infinito**.
2. Usa-se uma **fila de prioridade** (`heapq`) para processar **primeiro as cidades mais baratas**.
3. Para cada cidade vizinha, verifica-se se **o novo custo é menor** do que o previamente armazenado.
4. Caso o novo custo seja menor, ele é atualizado e a cidade é adicionada à fila de prioridade.
5. O processo repete até que **todas as cidades tenham sido processadas**.

### 🔹 **Complexidade Computacional**
A implementação com **fila de prioridade (`heapq`)** tem complexidade **O((V + E) log V)**, onde:
- `V` → Número de cidades.
- `E` → Número de estradas.

---

## 🛠 **Modelagem do Problema**

A rede rodoviária é modelada como um **grafo não-direcionado**, onde cada **cidade** é um **vértice** e cada **estrada** é uma **aresta** ponderada com **custo total da viagem (pedágios + combustível).**

A estrutura de dados utilizada é um **dicionário de adjacências**, onde cada **chave** representa uma cidade e os **valores** são listas contendo cidades vizinhas e seus custos.

### **Exemplo de Representação**
```python
malha = {
    "São Paulo": [("Campinas", 50), ("Ribeirão Preto", 150)],
    "Campinas": [("São Paulo", 50), ("Ribeirão Preto", 80), ("Bauru", 120)],
    "Ribeirão Preto": [("São Paulo", 150), ("Campinas", 80), ("Bauru", 90)],
    "Bauru": [("Campinas", 120), ("Ribeirão Preto", 90), ("Presidente Prudente", 110)],
    "Presidente Prudente": [("Bauru", 110), ("Ribeirão Preto", 170)]
}
```

---

## 🚀 **Implementação do Algoritmo**

A implementação está dividida em três módulos principais:

### 🔹 **1. Classe `MalhaRodoviaria`**
Essa classe **armazena e gerencia as cidades e as estradas**.

```python
class MalhaRodoviaria:
    def __init__(self):
        self.cidades = {}

    def adicionar_estrada(self, origem: str, destino: str, custo: float):
        """ Adiciona uma conexão entre cidades com um custo associado. """
        if origem not in self.cidades:
            self.cidades[origem] = []
        if destino not in self.cidades:
            self.cidades[destino] = []
        self.cidades[origem].append((destino, custo))
        self.cidades[destino].append((origem, custo))
```

---

### 🔹 **2. Algoritmo de Dijkstra**
A função `dijkstra()` calcula o **caminho mais barato** a partir da cidade de origem.

```python
import heapq

def dijkstra(self, origem: str):
    """ Calcula a rota mais barata entre cidades. """
    custos = {cidade: float('inf') for cidade in self.cidades}
    custos[origem] = 0
    caminho_anterior = {cidade: None for cidade in self.cidades}
    fila_prioridade = [(0, origem)]

    while fila_prioridade:
        custo_atual, cidade_atual = heapq.heappop(fila_prioridade)

        for vizinho, custo_viagem in self.cidades[cidade_atual]:
            novo_custo = custo_atual + custo_viagem
            if novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                caminho_anterior[vizinho] = cidade_atual
                heapq.heappush(fila_prioridade, (novo_custo, vizinho))

    return custos, caminho_anterior
```

---

### 🔹 **3. Reconstrução do Menor Caminho**
A função `rota_mais_barata()` permite **reconstruir o trajeto mais econômico**.

```python
def rota_mais_barata(self, origem: str, destino: str):
    """ Retorna o menor trajeto e o custo total. """
    custos, caminho_anterior = self.dijkstra(origem)
    caminho = []
    cidade_atual = destino

    while cidade_atual:
        caminho.insert(0, cidade_atual)
        cidade_atual = caminho_anterior[cidade_atual]

    return caminho, custos[destino]
```

---

## 📊 **Testes e Resultados**
O seguinte teste verifica a implementação:

```python
if __name__ == "__main__":
    malha = MalhaRodoviaria()
    malha.adicionar_estrada("São Paulo", "Campinas", 50)
    malha.adicionar_estrada("São Paulo", "Ribeirão Preto", 150)
    malha.adicionar_estrada("Campinas", "Ribeirão Preto", 80)
    malha.adicionar_estrada("Campinas", "Bauru", 120)
    malha.adicionar_estrada("Ribeirão Preto", "Bauru", 90)
    malha.adicionar_estrada("Bauru", "Presidente Prudente", 110)
    malha.adicionar_estrada("Ribeirão Preto", "Presidente Prudente", 170)

    origem = "São Paulo"
    destino = "Presidente Prudente"

    custos, _ = malha.dijkstra(origem)
    caminho, custo_total = malha.rota_mais_barata(origem, destino)

    print(f"\n📍 **Menores custos a partir de {origem}:**")
    for cidade, custo in custos.items():
        print(f"➡️ {cidade}: R$ {custo:.2f}")

    print(f"\n🚛 **Melhor rota de {origem} até {destino}:** {caminho}")
    print(f"💰 **Custo total:** R$ {custo_total:.2f}")
```

---

## 🔎 **Conclusão**
A aplicação do **Algoritmo de Dijkstra** permitiu determinar a **rota mais econômica para transporte de mercadorias**.
