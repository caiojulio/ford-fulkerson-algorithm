from collections import defaultdict

# Classe que representa o grafo
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  # Grafo residual
        self.V = vertices  # Número de vértices

    # Adiciona aresta ao grafo
    def add_edge(self, u, v, w):
        self.graph[u].append([v, w])  # u -> v com capacidade w

    # Implementação da busca em largura (BFS) para encontrar um caminho
    # de s a t no grafo residual
    def bfs(self, s, t, parent):
        visited = [False] * self.V
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v, capacity in self.graph[u]:
                if visited[v] is False and capacity > 0:  # Se ainda há capacidade disponível
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

                    if v == t:
                        return True
        return False

    # Algoritmo de Ford-Fulkerson
    def ford_fulkerson(self, source, sink):
        parent = [-1] * self.V  # Array para armazenar o caminho
        max_flow = 0  # Inicializando o fluxo máximo

        # Aumenta o fluxo enquanto há caminho no grafo residual
        while self.bfs(source, sink, parent):
            # Encontrando a capacidade mínima residual ao longo do caminho
            path_flow = float("Inf")
            s = sink
            while s != source:
                for v, capacity in self.graph[parent[s]]:
                    if v == s:
                        path_flow = min(path_flow, capacity)
                s = parent[s]

            # Atualizando as capacidades residuais das arestas e suas reversas
            v = sink
            while v != source:
                u = parent[v]
                for index, (vertex, capacity) in enumerate(self.graph[u]):
                    if vertex == v:
                        self.graph[u][index][1] -= path_flow  # Subtrai capacidade
                for index, (vertex, capacity) in enumerate(self.graph[v]):
                    if vertex == u:
                        self.graph[v][index][1] += path_flow  # Adiciona capacidade reversa
                v = parent[v]

            # Soma o fluxo atual ao fluxo total
            max_flow += path_flow

        return max_flow


# Exemplo de uso:
g = Graph(6)
g.add_edge(0, 1, 16)
g.add_edge(0, 2, 13)
g.add_edge(1, 2, 10)
g.add_edge(1, 3, 12)
g.add_edge(2, 1, 4)
g.add_edge(2, 4, 14)
g.add_edge(3, 2, 9)
g.add_edge(3, 5, 20)
g.add_edge(4, 3, 7)
g.add_edge(4, 5, 4)

source = 0  # Fonte
sink = 5    # Sumidouro

print(f"O fluxo máximo é: {g.ford_fulkerson(source, sink)}")
