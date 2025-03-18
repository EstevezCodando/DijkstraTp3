# ✈️ **Transporte Aéreo Internacional - Algoritmo de Dijkstra**

## 📖 **Introdução**

A crescente demanda por **passagens aéreas mais econômicas e eficientes** levou as companhias aéreas a investir em **sistemas inteligentes de roteamento**. O planejamento de voos deve levar em consideração **custos de passagens, taxas aeroportuárias, escalas obrigatórias e tempos de conexão** para oferecer a melhor experiência ao passageiro.

Este estudo apresenta uma implementação do **Algoritmo de Dijkstra Modificado** para encontrar a **rota aérea mais econômica**, considerando:
- **Custo total da viagem** → Inclui tarifas, taxas e impostos.
- **Escalas obrigatórias** → Algumas conexões podem ter custos extras fixos.
- **Tempo máximo de conexão** → Passageiros podem definir o tempo máximo permitido para conexões.

O objetivo é desenvolver um sistema **eficiente e modular** que permita encontrar a melhor rota entre dois aeroportos, respeitando restrições logísticas e preferências dos passageiros.

---

## 📚 **Fundamentação Teórica**

O **Algoritmo de Dijkstra** é um dos métodos mais utilizados para encontrar o **caminho de menor custo em um grafo ponderado**. Neste caso, o grafo representa a **rede de voos internacionais**, onde:
- **Os vértices (nós)** são **aeroportos**.
- **As arestas (ligações entre nós)** representam **voos diretos**.
- **Os pesos das arestas** indicam o **custo total do voo (tarifa + taxas + impostos).**

### 🔹 **Modificações no Algoritmo**
A implementação foi modificada para considerar:
1. **Escalas obrigatórias** → Adicionam um custo fixo ao voo.
2. **Tempo máximo de conexão** → Filtra voos com tempos de espera superiores ao permitido.
3. **Fila de prioridade (`heapq`)** → Para garantir eficiência no processamento.

### 🔹 **Complexidade Computacional**
A implementação com **fila de prioridade (`heapq`)** tem complexidade **O((V + E) log V)**, onde:
- `V` → Número de aeroportos.
- `E` → Número de conexões (voos diretos).

---

## 🛠 **Modelagem do Problema**

A malha aérea é representada como um **grafo ponderado**, onde **cada aeroporto é um vértice** e **cada voo é uma aresta** ponderada com o **custo total da viagem**.

Adicionalmente:
- Algumas rotas incluem **escalas obrigatórias**, que adicionam um **custo extra**.
- O passageiro pode definir um **tempo máximo permitido para conexões**.
- Utiliza-se uma **fila de prioridade (`heapq`)** para garantir que os voos mais baratos sejam processados primeiro.

### **Exemplo de Representação**
```python
rede = {
    "JFK": [("LHR", 500, 2), ("CDG", 550, 3)],
    "LHR": [("FRA", 200, 1), ("DXB", 600, 5)],
    "CDG": [("DXB", 650, 4)],
    "FRA": [("DXB", 300, 2), ("HKG", 800, 5)],
    "DXB": [("HKG", 700, 6)]
}
```
Onde:
- `"JFK"` e `"LHR"` são aeroportos.
- O voo `"JFK → LHR"` tem custo **$500** e tempo de conexão **2 horas**.
- `"FRA"` possui uma **escala obrigatória** com **custo extra de $50**.

---

## 🚀 **Implementação do Algoritmo**

A implementação é dividida em três partes:

### 🔹 **1. Classe `RedeAereaInternacional`**
Essa classe representa a **rede de voos internacionais** e gerencia aeroportos e conexões.

```python
class RedeAereaInternacional:
    def __init__(self):
        self.aeroportos = {}
        self.escalas_obrigatorias = {}  # Custos extras de escalas obrigatórias

    def adicionar_voo(self, origem: str, destino: str, custo: float, tempo_conexao: float):
        """ Adiciona um voo entre aeroportos com custo e tempo de conexão. """
        if origem not in self.aeroportos:
            self.aeroportos[origem] = []
        if destino not in self.aeroportos:
            self.aeroportos[destino] = []

        self.aeroportos[origem].append((destino, custo, tempo_conexao))
        self.aeroportos[destino].append((origem, custo, tempo_conexao))  # Grafo não-direcionado

    def adicionar_escala_obrigatoria(self, aeroporto: str, custo_extra: float):
        """ Adiciona um custo extra para escalas obrigatórias. """
        self.escalas_obrigatorias[aeroporto] = custo_extra
```

---

### 🔹 **2. Algoritmo de Dijkstra Modificado**
A função `dijkstra_modificado()` encontra a **rota mais barata** considerando custos, escalas obrigatórias e tempo máximo de conexão.

```python
import heapq

def dijkstra_modificado(self, origem: str, destino: str, tempo_maximo_conexao: float):
    """ Encontra a rota mais barata considerando tempo de conexão e escalas obrigatórias. """
    custos_minimos = {aeroporto: float('inf') for aeroporto in self.aeroportos}
    custos_minimos[origem] = 0
    caminho_anterior = {aeroporto: None for aeroporto in self.aeroportos}

    fila_prioridade = [(0, origem)]  # (custo acumulado, aeroporto)

    while fila_prioridade:
        custo_atual, aeroporto_atual = heapq.heappop(fila_prioridade)

        if aeroporto_atual == destino:
            break  # Chegamos ao destino

        for vizinho, custo_voo, tempo_conexao in self.aeroportos[aeroporto_atual]:
            if tempo_conexao > tempo_maximo_conexao:
                continue  # Ignorar voos que excedam o tempo máximo permitido

            custo_total = custo_atual + custo_voo

            if vizinho in self.escalas_obrigatorias:
                custo_total += self.escalas_obrigatorias[vizinho]

            if custo_total < custos_minimos[vizinho]:
                custos_minimos[vizinho] = custo_total
                caminho_anterior[vizinho] = aeroporto_atual
                heapq.heappush(fila_prioridade, (custo_total, vizinho))

    return custos_minimos, caminho_anterior
```

---

### 🔹 **3. Reconstrução do Menor Caminho**
A função `menor_rota()` retorna a melhor rota, considerando o custo total e o tempo máximo de conexão.

```python
def menor_rota(self, origem: str, destino: str, tempo_maximo_conexao: float):
    """ Retorna a melhor rota e o custo total. """
    custos_minimos, caminho_anterior = self.dijkstra_modificado(origem, destino, tempo_maximo_conexao)
    caminho = []
    aeroporto_atual = destino

    while aeroporto_atual:
        caminho.insert(0, aeroporto_atual)
        aeroporto_atual = caminho_anterior[aeroporto_atual]

    return caminho, custos_minimos[destino]
```

---

## 📊 **Testes e Resultados**
Para o seguinte **grafo de voos**:
```
JFK --$500, 2h--> LHR
JFK --$550, 3h--> CDG
LHR --$200, 1h--> FRA
LHR --$600, 5h--> DXB
FRA --$800, 5h--> HKG
DXB --$700, 6h--> HKG
```
Escalas obrigatórias:
- FRA: **+50 USD**
Tempo máximo de conexão: **3 horas**

**Saída esperada:**
```
✈️ Melhor rota de JFK até HKG: ['JFK', 'LHR', 'FRA', 'HKG']
💰 Custo total estimado: $1550.00
```

---

## 🔎 **Conclusão**
A implementação do **Dijkstra Modificado** possibilitou a **escolha da rota aérea mais econômica**, garantindo:
