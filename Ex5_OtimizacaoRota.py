import heapq

class CidadeInteligente:
    """ Representação da cidade como um grafo onde cada vértice é um cruzamento e cada aresta é uma rua. """

    def __init__(self):
        self.cruzamentos = {}
        self.estacoes_recarga = set()  # Conjunto de cruzamentos que possuem estações de recarga

    def adicionar_rua(self, origem: str, destino: str, tempo: float, distancia: float):
        """ Adiciona uma rua bidirecional entre dois cruzamentos. """
        if origem not in self.cruzamentos:
            self.cruzamentos[origem] = []
        if destino not in self.cruzamentos:
            self.cruzamentos[destino] = []
        
        self.cruzamentos[origem].append((destino, tempo, distancia))
        self.cruzamentos[destino].append((origem, tempo, distancia))  # Grafo não-direcionado

    def adicionar_estacao_recarga(self, cruzamento: str):
        """ Marca um cruzamento como tendo uma estação de recarga. """
        self.estacoes_recarga.add(cruzamento)

    def dijkstra_modificado(self, origem: str, destino: str, autonomia: float):
        """
        Aplica o Algoritmo de Dijkstra modificado para encontrar a melhor rota considerando tempo e recarga.
        """
        tempo_minimo = {cruzamento: float('inf') for cruzamento in self.cruzamentos}
        tempo_minimo[origem] = 0
        caminho_anterior = {cruzamento: None for cruzamento in self.cruzamentos}
        bateria_restante = {cruzamento: 0 for cruzamento in self.cruzamentos}
        bateria_restante[origem] = autonomia  # Início com bateria cheia

        fila_prioridade = [(0, origem, autonomia)]  # (tempo acumulado, cruzamento atual, bateria disponível)

        while fila_prioridade:
            tempo_atual, cruzamento_atual, bateria_atual = heapq.heappop(fila_prioridade)

            if cruzamento_atual == destino:
                break  # Chegamos ao destino

            for vizinho, tempo_rua, distancia_rua in self.cruzamentos[cruzamento_atual]:
                nova_bateria = bateria_atual - distancia_rua

                # Se não houver bateria suficiente, verificar estação de recarga
                if nova_bateria < 0:
                    if cruzamento_atual in self.estacoes_recarga:
                        nova_bateria = autonomia  # Recarga completa
                    else:
                        continue  # Ignorar esse caminho porque não há bateria suficiente

                novo_tempo = tempo_atual + tempo_rua

                if novo_tempo < tempo_minimo[vizinho]:
                    tempo_minimo[vizinho] = novo_tempo
                    caminho_anterior[vizinho] = cruzamento_atual
                    bateria_restante[vizinho] = nova_bateria
                    heapq.heappush(fila_prioridade, (novo_tempo, vizinho, nova_bateria))

        return tempo_minimo, caminho_anterior

    def melhor_rota(self, origem: str, destino: str, autonomia: float):
        """
        Retorna a melhor rota e tempo total considerando o tempo de deslocamento e necessidade de recarga.
        """
        tempo_minimo, caminho_anterior = self.dijkstra_modificado(origem, destino, autonomia)

        if tempo_minimo[destino] == float('inf'):
            return f"Não há rota viável entre {origem} e {destino} com essa autonomia."

        caminho = []
        cruzamento_atual = destino
        while cruzamento_atual:
            caminho.insert(0, cruzamento_atual)
            cruzamento_atual = caminho_anterior[cruzamento_atual]

        return caminho, tempo_minimo[destino]

# Teste do Algoritmo
if __name__ == "__main__":
    cidade = CidadeInteligente()

    # Definição dos cruzamentos, ruas e tempo de deslocamento (tempo em minutos, distância em km)
    cidade.adicionar_rua("A", "B", 5, 2)
    cidade.adicionar_rua("A", "C", 8, 3)
    cidade.adicionar_rua("B", "D", 7, 4)
    cidade.adicionar_rua("C", "D", 2, 1)
    cidade.adicionar_rua("C", "E", 10, 5)
    cidade.adicionar_rua("D", "E", 3, 2)

    # Adicionando estações de recarga
    cidade.adicionar_estacao_recarga("C")
    cidade.adicionar_estacao_recarga("D")

    # Definição da autonomia do veículo elétrico (em km)
    autonomia = 4

    # Encontrando a melhor rota entre dois cruzamentos
    origem = "A"
    destino = "E"
    caminho, tempo_total = cidade.melhor_rota(origem, destino, autonomia)

    print(f"\n📍 **Melhores tempos de deslocamento a partir de {origem}:**")
    tempos, _ = cidade.dijkstra_modificado(origem, destino, autonomia)
    for cruzamento, tempo in tempos.items():
        print(f"➡️ {cruzamento}: {tempo:.2f} min")

    print(f"\n🚗 **Melhor rota de {origem} até {destino}:** {caminho}")
    print(f"⏱ **Tempo total estimado:** {tempo_total:.2f} min")
