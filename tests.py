def bfs(graph, residual_graph, parent, source, sink):
    visited = [False] * len(graph)
    queue = []
    queue.append(source)
    visited[source] = True

    while queue:
        u = queue.pop(0)
        for v, capacity in enumerate(residual_graph[u]):
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

def ford_fulkerson(graph, source, sink, lower_limits):
    max_flow = 0
    parent = [-1] * len(graph)
    
    residual_graph = [row[:] for row in graph]

    while bfs(graph, residual_graph, parent, source, sink):
        path_flow = float('inf')
        s = sink
        while(s != source):
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        v = sink
        while(v != source):
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]

        # Check if the flow on any edge violates the lower limit constraint
        for u in range(len(graph)):
            for v in range(len(graph[u])):
                if graph[u][v] > 0 and residual_graph[u][v] < graph[u][v] and graph[u][v] - residual_graph[u][v] < lower_limits[u][v]:
                    # If lower limit constraint is violated, reset flow to lower limit
                    residual_graph[u][v] = graph[u][v]

        max_flow += path_flow

    return max_flow, graph



# Example usage:
# Define the graph as an adjacency matrix
graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

# Lower limits for each edge
lower_limits = [
    [0, 100 , 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

source = 0
sink = 5

max_flow, residual_graph = ford_fulkerson(graph, source, sink, lower_limits)
print("Max Flow:", max_flow)
print("Residual Graph:", residual_graph)
