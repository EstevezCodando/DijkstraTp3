import heapq

class MalhaRodoviaria:
    """ Representação da rede de transporte rodoviário entre cidades. """

    def __init__(self):
        self.cidades = {}

    def adicionar_estrada(self, origem: str, destino: str, custo: float):
        """ Adiciona uma conexão entre duas cidades com um custo associado. """
        if origem not in self.cidades:
            self.cidades[origem] = []
        if destino not in self.cidades:
            self.cidades[destino] = []

        self.cidades[origem].append((destino, custo))
        self.cidades[destino].append((origem, custo))  # Grafo não-direcionado

    def dijkstra(self, origem: str):
        """
        Aplica o Algoritmo de Dijkstra para encontrar o menor custo
        entre a cidade de origem e as demais.
        """
        custos = {cidade: float('inf') for cidade in self.cidades}
        custos[origem] = 0
        caminho_anterior = {cidade: None for cidade in self.cidades}

        fila_prioridade = [(0, origem)]  # (custo acumulado, cidade)

        while fila_prioridade:
            custo_atual, cidade_atual = heapq.heappop(fila_prioridade)

            if custo_atual > custos[cidade_atual]:
                continue

            for vizinho, custo_viagem in self.cidades[cidade_atual]:
                novo_custo = custo_atual + custo_viagem
                if novo_custo < custos[vizinho]:
                    custos[vizinho] = novo_custo
                    caminho_anterior[vizinho] = cidade_atual
                    heapq.heappush(fila_prioridade, (novo_custo, vizinho))

        return custos, caminho_anterior

    def rota_mais_barata(self, origem: str, destino: str):
        """
        Retorna o menor caminho e o custo total entre duas cidades.
        """
        custos, caminho_anterior = self.dijkstra(origem)

        if custos[destino] == float('inf'):
            return f"Não há rota entre {origem} e {destino}."

        caminho = []
        cidade_atual = destino
        while cidade_atual:
            caminho.insert(0, cidade_atual)
            cidade_atual = caminho_anterior[cidade_atual]

        return caminho, custos[destino]

# Teste do Algoritmo
if __name__ == "__main__":
    malha = MalhaRodoviaria()

    # Definição das cidades e custos de viagem (pedágios + combustível)
    malha.adicionar_estrada("São Paulo", "Campinas", 50)
    malha.adicionar_estrada("São Paulo", "Ribeirão Preto", 150)
    malha.adicionar_estrada("Campinas", "Ribeirão Preto", 80)
    malha.adicionar_estrada("Campinas", "Bauru", 120)
    malha.adicionar_estrada("Ribeirão Preto", "Bauru", 90)
    malha.adicionar_estrada("Bauru", "Presidente Prudente", 110)
    malha.adicionar_estrada("Ribeirão Preto", "Presidente Prudente", 170)

    # Encontrando a rota mais barata entre duas cidades
    origem = "São Paulo"
    destino = "Presidente Prudente"
    caminho, custo_total = malha.rota_mais_barata(origem, destino)

    print(f"\n📍 **Menores custos a partir de {origem}:**")
    custos, _ = malha.dijkstra(origem)
    for cidade, custo in custos.items():
        print(f"➡️ {cidade}: R$ {custo:.2f}")

    print(f"\n🚛 **Melhor rota de {origem} até {destino}:** {caminho}")
    print(f"💰 **Custo total:** R$ {custo_total:.2f}")
