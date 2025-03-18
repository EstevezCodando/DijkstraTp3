import heapq

class RedeAereaInternacional:
    """ Representação do sistema de voos internacionais como um grafo ponderado. """

    def __init__(self):
        self.aeroportos = {}
        self.escalas_obrigatorias = {}  # Dicionário para armazenar custos extras de escalas
        self.tempos_de_conexao = {}  # Dicionário com tempos de conexão entre aeroportos

    def adicionar_voo(self, origem: str, destino: str, custo: float, tempo_conexao: float):
        """ Adiciona um voo entre aeroportos com custo e tempo de conexão. """
        if origem not in self.aeroportos:
            self.aeroportos[origem] = []
        if destino not in self.aeroportos:
            self.aeroportos[destino] = []

        self.aeroportos[origem].append((destino, custo, tempo_conexao))
        self.aeroportos[destino].append((origem, custo, tempo_conexao))  # Grafo não-direcionado

    def adicionar_escala_obrigatoria(self, aeroporto: str, custo_extra: float):
        """ Adiciona um custo fixo para escalas obrigatórias em um aeroporto específico. """
        self.escalas_obrigatorias[aeroporto] = custo_extra

    def dijkstra_modificado(self, origem: str, destino: str, tempo_maximo_conexao: float):
        """
        Aplica o Algoritmo de Dijkstra modificado para encontrar a rota de menor custo,
        considerando escalas obrigatórias e tempo máximo de conexão.
        """
        custos_minimos = {aeroporto: float('inf') for aeroporto in self.aeroportos}
        custos_minimos[origem] = 0
        caminho_anterior = {aeroporto: None for aeroporto in self.aeroportos}

        fila_prioridade = [(0, origem)]  # (custo acumulado, aeroporto atual)

        while fila_prioridade:
            custo_atual, aeroporto_atual = heapq.heappop(fila_prioridade)

            if aeroporto_atual == destino:
                break  # Chegamos ao destino

            for vizinho, custo_voo, tempo_conexao in self.aeroportos[aeroporto_atual]:
                # Ignorar voos que excedem o tempo máximo de conexão permitido
                if tempo_conexao > tempo_maximo_conexao:
                    continue

                custo_total = custo_atual + custo_voo

                # Adicionar custo extra se for uma escala obrigatória
                if vizinho in self.escalas_obrigatorias:
                    custo_total += self.escalas_obrigatorias[vizinho]

                if custo_total < custos_minimos[vizinho]:
                    custos_minimos[vizinho] = custo_total
                    caminho_anterior[vizinho] = aeroporto_atual
                    heapq.heappush(fila_prioridade, (custo_total, vizinho))

        return custos_minimos, caminho_anterior

    def menor_rota(self, origem: str, destino: str, tempo_maximo_conexao: float):
        """
        Retorna a menor rota considerando o custo total e as restrições de escalas.
        """
        custos_minimos, caminho_anterior = self.dijkstra_modificado(origem, destino, tempo_maximo_conexao)

        if custos_minimos[destino] == float('inf'):
            return f"Não há rota viável entre {origem} e {destino} respeitando o tempo máximo de conexão."

        caminho = []
        aeroporto_atual = destino
        while aeroporto_atual:
            caminho.insert(0, aeroporto_atual)
            aeroporto_atual = caminho_anterior[aeroporto_atual]

        return caminho, custos_minimos[destino]

# Teste do Algoritmo
if __name__ == "__main__":
    rede = RedeAereaInternacional()

    # Definição das rotas internacionais (aeroportos, custos e tempos de conexão)
    rede.adicionar_voo("JFK", "LHR", 500, 2)
    rede.adicionar_voo("JFK", "CDG", 550, 3)
    rede.adicionar_voo("LHR", "FRA", 200, 1)
    rede.adicionar_voo("LHR", "DXB", 600, 5)
    rede.adicionar_voo("CDG", "DXB", 650, 4)
    rede.adicionar_voo("FRA", "DXB", 300, 2)
    rede.adicionar_voo("DXB", "HKG", 700, 6)
    rede.adicionar_voo("FRA", "HKG", 800, 5)

    # Definição de escalas obrigatórias com custos adicionais
    rede.adicionar_escala_obrigatoria("FRA", 50)  # Frankfurt adiciona um custo extra de escala

    # Definição do tempo máximo permitido para conexões
    tempo_max_conexao = 3  # Máximo de 3 horas de espera em conexões

    # Encontrando a melhor rota entre dois aeroportos
    origem = "JFK"
    destino = "HKG"
    caminho, custo_total = rede.menor_rota(origem, destino, tempo_max_conexao)

    print(f"\n📍 **Menores custos a partir do aeroporto {origem}:**")
    custos, _ = rede.dijkstra_modificado(origem, destino, tempo_max_conexao)
    for aeroporto, custo in custos.items():
        print(f"➡️ {aeroporto}: ${custo:.2f}")

    print(f"\n✈️ **Melhor rota de {origem} até {destino}:** {caminho}")
    print(f"💰 **Custo total estimado:** ${custo_total:.2f}")
