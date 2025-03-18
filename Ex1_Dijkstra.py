import heapq

class Grafo:
    """ Representação de um grafo para modelar a logística de entregas. """

    def __init__(self):
        self.vertices = {}

    def adicionar_aresta(self, origem: str, destino: str, distancia: float):
        """ Adiciona uma aresta bidirecional entre dois bairros. """
        if origem not in self.vertices:
            self.vertices[origem] = []
        if destino not in self.vertices:
            self.vertices[destino] = []

        self.vertices[origem].append((destino, distancia))
        self.vertices[destino].append((origem, distancia))  # Grafo não-direcionado

    def dijkstra(self, origem: str):
        """
        Aplica o algoritmo de Dijkstra para encontrar a menor distância
        do centro de distribuição (origem) para todos os bairros.
        """
        distancias = {bairro: float('inf') for bairro in self.vertices}
        distancias[origem] = 0
        caminho_anterior = {bairro: None for bairro in self.vertices}

        fila_prioridade = [(0, origem)]  # (distância acumulada, bairro)

        while fila_prioridade:
            distancia_atual, bairro_atual = heapq.heappop(fila_prioridade)

            # Se a distância atual é maior que a armazenada, ignore (otimização)
            if distancia_atual > distancias[bairro_atual]:
                continue

            for vizinho, peso in self.vertices[bairro_atual]:
                distancia_nova = distancia_atual + peso
                if distancia_nova < distancias[vizinho]:
                    distancias[vizinho] = distancia_nova
                    caminho_anterior[vizinho] = bairro_atual
                    heapq.heappush(fila_prioridade, (distancia_nova, vizinho))

        return distancias, caminho_anterior

    def menor_caminho(self, origem: str, destino: str):
        """
        Reconstrói o menor caminho do centro de distribuição até um bairro específico.
        """
        distancias, caminho_anterior = self.dijkstra(origem)

        if distancias[destino] == float('inf'):
            return f"Não há caminho entre {origem} e {destino}."

        caminho = []
        bairro_atual = destino
        while bairro_atual:
            caminho.insert(0, bairro_atual)
            bairro_atual = caminho_anterior[bairro_atual]

        return caminho, distancias[destino]

# Teste do Algoritmo
if __name__ == "__main__":
    grafo = Grafo()

    # Definição dos bairros e distâncias entre eles
    grafo.adicionar_aresta("Centro", "Bairro A", 4)
    grafo.adicionar_aresta("Centro", "Bairro B", 2)
    grafo.adicionar_aresta("Bairro A", "Bairro B", 5)
    grafo.adicionar_aresta("Bairro A", "Bairro C", 10)
    grafo.adicionar_aresta("Bairro B", "Bairro C", 3)
    grafo.adicionar_aresta("Bairro C", "Bairro D", 8)
    grafo.adicionar_aresta("Bairro B", "Bairro D", 7)

    # Encontrando o menor caminho do Centro para todos os bairros
    origem = "Centro"
    distancias, _ = grafo.dijkstra(origem)

    print(f"\n📍 **Menores distâncias do {origem} até cada bairro:**")
    for bairro, distancia in distancias.items():
        print(f"➡️ {bairro}: {distancia} km")

    # Encontrando o menor caminho para um bairro específico
    destino = "Bairro D"
    caminho, distancia_total = grafo.menor_caminho(origem, destino)

    print(f"\n🛣 **Menor caminho de {origem} até {destino}:** {caminho}")
    print(f"📏 **Distância total:** {distancia_total} km")
