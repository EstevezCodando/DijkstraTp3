import heapq

class Grafo:
    """ Representação de um grafo para modelar o sistema de roteamento de ônibus. """

    def __init__(self):
        self.vertices = {}

    def adicionar_aresta(self, origem: str, destino: str, tempo: float):
        """ Adiciona uma aresta bidirecional representando o tempo médio de deslocamento entre dois bairros. """
        if origem not in self.vertices:
            self.vertices[origem] = []
        if destino not in self.vertices:
            self.vertices[destino] = []

        self.vertices[origem].append((destino, tempo))
        self.vertices[destino].append((origem, tempo))  # Grafo não-direcionado

    def dijkstra(self, origem: str):
        """
        Aplica o algoritmo de Dijkstra para encontrar o menor tempo de deslocamento
        entre o bairro de origem e os demais bairros da cidade.
        """
        tempos = {bairro: float('inf') for bairro in self.vertices}
        tempos[origem] = 0
        caminho_anterior = {bairro: None for bairro in self.vertices}

        fila_prioridade = [(0, origem)]  # (tempo acumulado, bairro)

        while fila_prioridade:
            tempo_atual, bairro_atual = heapq.heappop(fila_prioridade)

            if tempo_atual > tempos[bairro_atual]:
                continue

            for vizinho, peso in self.vertices[bairro_atual]:
                novo_tempo = tempo_atual + peso
                if novo_tempo < tempos[vizinho]:
                    tempos[vizinho] = novo_tempo
                    caminho_anterior[vizinho] = bairro_atual
                    heapq.heappush(fila_prioridade, (novo_tempo, vizinho))

        return tempos, caminho_anterior

    def menor_caminho(self, origem: str, destino: str):
        """
        Retorna o menor caminho em tempo entre dois bairros e a duração total.
        """
        tempos, caminho_anterior = self.dijkstra(origem)

        if tempos[destino] == float('inf'):
            return f"Não há trajeto entre {origem} e {destino}."

        caminho = []
        bairro_atual = destino
        while bairro_atual:
            caminho.insert(0, bairro_atual)
            bairro_atual = caminho_anterior[bairro_atual]

        return caminho, tempos[destino]

# Teste do Algoritmo
if __name__ == "__main__":
    grafo = Grafo()

    # Definição dos bairros e tempos médios de deslocamento (em minutos)
    grafo.adicionar_aresta("Bairro A", "Bairro B", 10)
    grafo.adicionar_aresta("Bairro A", "Bairro C", 15)
    grafo.adicionar_aresta("Bairro B", "Bairro D", 12)
    grafo.adicionar_aresta("Bairro B", "Bairro C", 5)
    grafo.adicionar_aresta("Bairro C", "Bairro D", 10)
    grafo.adicionar_aresta("Bairro C", "Bairro E", 5)
    grafo.adicionar_aresta("Bairro D", "Bairro E", 10)

    # Encontrando o menor tempo entre dois bairros movimentados
    origem = "Bairro A"
    destino = "Bairro E"
    caminho, tempo_total = grafo.menor_caminho(origem, destino)

    print(f"\n📍 **Menores tempos de deslocamento a partir de {origem}:**")
    tempos, _ = grafo.dijkstra(origem)
    for bairro, tempo in tempos.items():
        print(f"➡️ {bairro}: {tempo} minutos")

    print(f"\n🚌 **Menor trajeto de {origem} até {destino}:** {caminho}")
    print(f"⏱ **Tempo total de deslocamento:** {tempo_total} minutos")
