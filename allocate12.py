def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    
    total_size = 2
    total_size += len(preferences)
    total_size += len(officers_per_org) * 3
    graph = [[0 for i in range(total_size)] for j in range(total_size)]
    for i in range(1, len(preferences)+ 1):
        graph[0][i] = max_shifts
    for i in range(len(preferences)):
        if preferences[i][0] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 1] = 30 
        if preferences[i][1] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 2] = 30 
        if preferences[i][2] == 1:
            for j in range(len(officers_per_org)):
               graph[1 + i][len(preferences) + 3*j + 3] = 30 

    for i in range(len(officers_per_org)):
        graph[len(preferences) + 1 + i*3][len(graph) - 1] = officers_per_org[i][0] * 30
        graph[len(preferences) + 1 + i*3 + 1][len(graph) - 1] = officers_per_org[i][1] * 30
        graph[len(preferences) + 1 + i*3+2][len(graph) - 1] = officers_per_org[i][2] * 30
    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]
    ford_fulkerson(graph, 0, len(graph) - 1)
    
    JWS_graph = [[0 for i in range(len(preferences)*len(officers_per_org)*3 + 32)] for j in range(len(preferences)*len(officers_per_org)*3 + 32)]
    for i in range(len(officers_per_org)):
        for j in range(len(preferences)):
            print(i,j)
            JWS_graph[0][1+j*len(preferences) +i*len(preferences)] = max_shifts
            JWS_graph[0][1+j*len(preferences) +i*len(preferences) +1] = max_shifts
            JWS_graph[0][1+j*len(preferences) +i*len(preferences) +2] = max_shifts
    

    for i in JWS_graph:
        print(i)
    return allocations
    











def ford_fulkerson(graph, source, sink):
    def dfs(graph, source, sink, path, visited):
        if source == sink:
            return path
        visited[source] = True
        for neighbor, capacity in enumerate(graph[source]):
            if not visited[neighbor] and capacity > 0:
                augmenting_path = dfs(graph, neighbor, sink, path + [(source, neighbor)], visited)
                if augmenting_path is not None:
                    return augmenting_path
        return None

    max_flow = 0
    while True:
        # Find an augmenting path using DFS
        visited = [False] * len(graph)
        augmenting_path = dfs(graph, source, sink, [], visited)
        
        # If no augmenting path exists, terminate
        if augmenting_path is None:
            break
        
        # Find the bottleneck capacity along the augmenting path
        bottleneck = min(graph[u][v] for u, v in augmenting_path)
        
        # Update the residual capacities along the augmenting path
        for u, v in augmenting_path:
            graph[u][v] -= bottleneck
            graph[v][u] += bottleneck
        
        # Increment the max flow by the bottleneck capacity
        max_flow += bottleneck
    
    return max_flow



pref = [[0,0,1],
        [0,1,0],
        [1,0,0],
        [1,1,1]]
        

officer_per = [[1,1,1]]


a = allocate(pref, officer_per, 0, 25)
for i in a:
    print(i)