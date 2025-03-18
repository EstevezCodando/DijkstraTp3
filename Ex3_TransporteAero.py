import heapq

class RedeAerea:
    """ Representação da rede de aeroportos e distâncias diretas entre eles. """

    def __init__(self):
        self.aeroportos = {}

    def adicionar_rota(self, origem: str, destino: str, distancia: float):
        """ Adiciona uma conexão direta entre dois aeroportos. """
        if origem not in self.aeroportos:
            self.aeroportos[origem] = []
        if destino not in self.aeroportos:
            self.aeroportos[destino] = []

        self.aeroportos[origem].append((destino, distancia))
        self.aeroportos[destino].append((origem, distancia))  # Grafo não-direcionado

    def dijkstra(self, origem: str):
        """
        Aplica o Algoritmo de Dijkstra para encontrar a menor distância
        entre o aeroporto de origem e os demais da rede.
        """
        distancias = {aeroporto: float('inf') for aeroporto in self.aeroportos}
        distancias[origem] = 0
        caminho_anterior = {aeroporto: None for aeroporto in self.aeroportos}

        fila_prioridade = [(0, origem)]  # (distância acumulada, aeroporto)

        while fila_prioridade:
            distancia_atual, aeroporto_atual = heapq.heappop(fila_prioridade)

            if distancia_atual > distancias[aeroporto_atual]:
                continue

            for vizinho, peso in self.aeroportos[aeroporto_atual]:
                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    caminho_anterior[vizinho] = aeroporto_atual
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

        return distancias, caminho_anterior

    def menor_rota(self, origem: str, destino: str):
        """
        Retorna o menor caminho entre dois aeroportos e a distância total.
        """
        distancias, caminho_anterior = self.dijkstra(origem)

        if distancias[destino] == float('inf'):
            return f"Não há rota entre {origem} e {destino}."

        caminho = []
        aeroporto_atual = destino
        while aeroporto_atual:
            caminho.insert(0, aeroporto_atual)
            aeroporto_atual = caminho_anterior[aeroporto_atual]

        return caminho, distancias[destino]

# Teste do Algoritmo
if __name__ == "__main__":
    rede = RedeAerea()

    # Definição dos aeroportos e distâncias diretas (em km)
    rede.adicionar_rota("GRU", "GIG", 365)
    rede.adicionar_rota("GRU", "BSB", 873)
    rede.adicionar_rota("GIG", "CNF", 440)
    rede.adicionar_rota("BSB", "CNF", 624)
    rede.adicionar_rota("BSB", "SSA", 1060)
    rede.adicionar_rota("CNF", "SSA", 694)
    rede.adicionar_rota("SSA", "REC", 675)

    # Encontrando a menor rota entre dois aeroportos
    origem = "GRU"
    destino = "REC"
    caminho, distancia_total = rede.menor_rota(origem, destino)

    print(f"\n📍 **Menores distâncias a partir do aeroporto {origem}:**")
    distancias, _ = rede.dijkstra(origem)
    for aeroporto, distancia in distancias.items():
        print(f"➡️ {aeroporto}: {distancia} km")

    print(f"\n✈️ **Melhor rota de {origem} até {destino}:** {caminho}")
    print(f"📏 **Distância total:** {distancia_total} km")
