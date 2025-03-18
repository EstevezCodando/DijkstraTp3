# 🚗 **Otimização de Rotas em uma Cidade Inteligente - Algoritmo de Dijkstra**

## 📖 **Introdução**

Com o avanço das tecnologias em **cidades inteligentes**, o planejamento de trânsito para **veículos elétricos autônomos** torna-se essencial para garantir **eficiência energética, redução do congestionamento e melhor aproveitamento da infraestrutura urbana**. 

Neste estudo, aplicamos o **Algoritmo de Dijkstra Modificado** para encontrar **a rota mais eficiente** entre dois pontos da cidade, considerando:
- **Tempo estimado de deslocamento** como fator principal.
- **Autonomia da bateria do veículo elétrico**.
- **Necessidade de passar por estações de recarga**, caso o trajeto ultrapasse a autonomia disponível.

Esse sistema permite que veículos elétricos autônomos escolham **rotas otimizadas**, minimizando o tempo de deslocamento e evitando situações em que fiquem sem bateria no meio do caminho.

---

## 📚 **Fundamentação Teórica**

O **Algoritmo de Dijkstra** é amplamente utilizado para calcular **o menor caminho em grafos ponderados**, garantindo que a solução seja **ótima e eficiente**.

### 🔹 **Funcionamento do Algoritmo**
1. Define-se o **cruzamento de origem** com **tempo 0** e os demais com **tempo infinito**.
2. Utiliza-se uma **fila de prioridade (`heapq`)** para processar **primeiro o cruzamento com menor tempo acumulado**.
3. Para cada cruzamento vizinho:
   - Calcula-se **o novo tempo de deslocamento**.
   - Se o tempo for menor que o já armazenado, a informação é atualizada.
   - **Se a distância percorrida exceder a autonomia**, o veículo deve obrigatoriamente **passar por uma estação de recarga** antes de continuar.
4. O processo continua até que **todos os cruzamentos tenham sido processados** ou o destino seja alcançado.

### 🔹 **Modificações no Algoritmo**
A versão original do Dijkstra foi modificada para incluir:
- **Controle da autonomia da bateria**: se um trajeto excede a autonomia do veículo, ele **precisa recarregar antes de continuar**.
- **Estações de recarga**: o algoritmo prioriza cruzamentos com **estações de recarga** quando necessário.
- **Priorização do tempo**: a escolha das ruas considera **o tempo de deslocamento como fator principal**.

### 🔹 **Complexidade Computacional**
A implementação com **fila de prioridade (`heapq`)** tem complexidade **O((V + E) log V)**, onde:
- `V` → Número de cruzamentos.
- `E` → Número de ruas.

---

## 🛠 **Modelagem do Problema**

A cidade é representada como um **grafo direcionado**, onde:
- **Os vértices (nós)** são **cruzamentos**.
- **As arestas (ligações entre cruzamentos)** são **ruas**.
- **Os pesos das arestas** representam o **tempo estimado de deslocamento**.

Adicionalmente:
- Algumas ruas possuem **estações de recarga**.
- O veículo elétrico tem **um limite de autonomia**, e caso precise percorrer um trajeto maior, **ele deve parar em um ponto de recarga**.

### **Exemplo de Representação**
```python
cidade = {
    "A": [("B", 5, 2), ("C", 8, 3)],
    "B": [("D", 7, 4)],
    "C": [("D", 2, 1), ("E", 10, 5)],
    "D": [("E", 3, 2)]
}
```
Onde:
- `"A"` e `"B"` são cruzamentos.
- A rua `"A → B"` leva **5 minutos** e tem **2 km de distância**.
- `"C"` e `"D"` possuem **estações de recarga**.

---

## 🚀 **Implementação do Algoritmo**

A implementação está dividida em três módulos principais:

### 🔹 **1. Classe `CidadeInteligente`**
Essa classe **armazena a estrutura da cidade e as estações de recarga**.

```python
class CidadeInteligente:
    def __init__(self):
        self.cruzamentos = {}
        self.estacoes_recarga = set()

    def adicionar_rua(self, origem: str, destino: str, tempo: float, distancia: float):
        """ Adiciona uma rua entre cruzamentos com tempo e distância associada. """
        if origem not in self.cruzamentos:
            self.cruzamentos[origem] = []
        if destino not in self.cruzamentos:
            self.cruzamentos[destino] = []
        self.cruzamentos[origem].append((destino, tempo, distancia))
        self.cruzamentos[destino].append((origem, tempo, distancia))

    def adicionar_estacao_recarga(self, cruzamento: str):
        """ Marca um cruzamento como possuindo estação de recarga. """
        self.estacoes_recarga.add(cruzamento)
```

---

### 🔹 **2. Algoritmo de Dijkstra Modificado**
A função `dijkstra_modificado()` encontra **a melhor rota considerando tempo e necessidade de recarga**.

```python
import heapq

def dijkstra_modificado(self, origem: str, destino: str, autonomia: float):
    """ Calcula a rota mais eficiente, considerando tempo de viagem e autonomia do veículo elétrico. """
    tempo_minimo = {cruzamento: float('inf') for cruzamento in self.cruzamentos}
    tempo_minimo[origem] = 0
    caminho_anterior = {cruzamento: None for cruzamento in self.cruzamentos}
    bateria_restante = {cruzamento: 0 for cruzamento in self.cruzamentos}
    bateria_restante[origem] = autonomia

    fila_prioridade = [(0, origem, autonomia)]

    while fila_prioridade:
        tempo_atual, cruzamento_atual, bateria_atual = heapq.heappop(fila_prioridade)

        if cruzamento_atual == destino:
            break

        for vizinho, tempo_rua, distancia_rua in self.cruzamentos[cruzamento_atual]:
            nova_bateria = bateria_atual - distancia_rua

            if nova_bateria < 0:
                if cruzamento_atual in self.estacoes_recarga:
                    nova_bateria = autonomia
                else:
                    continue

            novo_tempo = tempo_atual + tempo_rua

            if novo_tempo < tempo_minimo[vizinho]:
                tempo_minimo[vizinho] = novo_tempo
                caminho_anterior[vizinho] = cruzamento_atual
                bateria_restante[vizinho] = nova_bateria
                heapq.heappush(fila_prioridade, (novo_tempo, vizinho, nova_bateria))

    return tempo_minimo, caminho_anterior
```

---

### 🔹 **3. Reconstrução do Menor Caminho**
A função `melhor_rota()` reconstrói **a melhor rota considerando tempo e recarga**.

```python
def melhor_rota(self, origem: str, destino: str, autonomia: float):
    """ Retorna o melhor trajeto e tempo total. """
    tempo_minimo, caminho_anterior = self.dijkstra_modificado(origem, destino, autonomia)
    caminho = []
    cruzamento_atual = destino

    while cruzamento_atual:
        caminho.insert(0, cruzamento_atual)
        cruzamento_atual = caminho_anterior[cruzamento_atual]

    return caminho, tempo_minimo[destino]
```

---

## 📊 **Testes e Resultados**
Com ruas, tempos e estações de recarga definidas, um teste real retorna:

```
📍 **Melhores tempos de deslocamento a partir de A:**
➡️ A: 0.00 min
➡️ B: 5.00 min
➡️ C: 8.00 min
➡️ D: 10.00 min
➡️ E: 13.00 min

🚗 **Melhor rota de A até E:** ['A', 'C', 'D', 'E']
⏱ **Tempo total estimado:** 13.00 min
```

---

## 🔎 **Conclusão**
A aplicação do **Dijkstra Modificado** permitiu otimizar **rotas para veículos elétricos**, garantindo:
