def allocate(preferences, officers_per_org, min_shifts, max_shifts):

    total_size = 5
    total_size += len(preferences)
    graph = [[0 for i in range(total_size)] for j in range(total_size)]
    for i in range(1, len(preferences)+ 1):
        graph[0][i] = max_shifts
    for i in range(len(preferences)):
        if preferences[i][0] == 1:
            graph[1 + i][len(preferences) + 1] = 30
        
        if preferences[i][1] == 1:
            graph[1+ i][len(preferences) + 2] = 30
        
        if preferences[i][2] == 1:
            graph[1+ i][len(preferences)+ 3] = 30

    shift1 = 0
    shift2 = 0
    shift3 = 0
    for j in officers_per_org:
        shift1 += j[0]
        shift2 += j[1]
        shift3 += j[2]
    shift3 = shift3 * 30
    shift2 = shift2 * 30
    shift1 = shift1 *30
    graph[len(preferences) + 1][len(graph) - 1] = shift1
    graph[len(preferences) + 2][len(graph) - 1] = shift2
    graph[len(preferences) + 3][len(graph) - 1] = shift3


    allocations = [[[[0,0,0] for k in range(30)] for i in range(len(officers_per_org))] for j in range(len(preferences))]
    for i in allocations:
        print(i)

    

    for i in officers_per_org:
        i[0] = i[0]*30
        i[1] = i[1]*30
        i[2] = i[2]*30


    flow = ford_fulkerson(graph, 0, len(graph) - 1)
    for workers in range(1, len(preferences) + 1):
        for jobs in range(len(officers_per_org)):
            for days in range(30):
                for shift in range(3):
                    allocations[workers][jobs][days][shift] = 



    for i in graph:
        print(i)
    print(allocations)
    return graph








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


source = 0
sink = 7
pref = [[0,1,1],
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [1,1,1]]
        

officer_per = [[0,1,1],
        [1,1,0]]


a = allocate(pref, officer_per, 0, 25)